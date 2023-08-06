from gettext import gettext as _
import logging
import asyncio
import aiohttp
import os
import shutil
import bz2
import gzip
import lzma
from collections import defaultdict
from tempfile import NamedTemporaryFile

from debian import deb822

from urllib.parse import urlparse, urlunparse

from pulpcore.plugin.exceptions import DigestValidationError
from pulpcore.plugin.models import Artifact, ProgressReport, Remote, Repository
from pulpcore.plugin.stages import (
    DeclarativeArtifact,
    DeclarativeContent,
    DeclarativeVersion,
    Stage,
    QueryExistingArtifacts,
    ArtifactDownloader,
    ArtifactSaver,
    QueryExistingContents,
    ContentSaver,
    RemoteArtifactSaver,
    ResolveContentFutures,
)

from pulp_deb.app.models import (
    GenericContent,
    ReleaseFile,
    PackageIndex,
    InstallerFileIndex,
    Package,
    InstallerPackage,
    DebRemote,
)

from pulp_deb.app.serializers import InstallerPackage822Serializer, Package822Serializer


log = logging.getLogger(__name__)


class NoPackageIndexFile(Exception):
    """
    Exception to signal, that no file representing a package index is present.
    """

    pass


def synchronize(remote_pk, repository_pk, mirror):
    """
    Sync content from the remote repository.

    Create a new version of the repository that is synchronized with the remote.

    Args:
        remote_pk (str): The remote PK.
        repository_pk (str): The repository PK.
        mirror (bool): True for mirror mode, False for additive.

    Raises:
        ValueError: If the remote does not specify a URL to sync

    """
    remote = DebRemote.objects.get(pk=remote_pk)
    repository = Repository.objects.get(pk=repository_pk)

    if not remote.url:
        raise ValueError(_("A remote must have a url specified to synchronize."))

    first_stage = DebFirstStage(remote)
    DebDeclarativeVersion(first_stage, repository, mirror=mirror).create()


class DeclarativeFailsafeArtifact(DeclarativeArtifact):
    """
    A declarative artifact that does not fail on 404.
    """

    async def download(self):
        """
        Download the artifact and set to None on 404.
        """
        try:
            await super().download()
        except aiohttp.client_exceptions.ClientResponseError as e:
            if e.code == 404:
                self.artifact = None
                log.info("Artifact not found. Ignored")
            else:
                raise
        except DigestValidationError:
            self.artifact = None
            log.info("Artifact digest not matched. Ignored")


class DebDeclarativeVersion(DeclarativeVersion):
    """
    This class creates the Pipeline.
    """

    def pipeline_stages(self, new_version):
        """
        Build the list of pipeline stages feeding into the ContentAssociation stage.

        Args:
            new_version (:class:`~pulpcore.plugin.models.RepositoryVersion`): The
                new repository version that is going to be built.

        Returns:
            list: List of :class:`~pulpcore.plugin.stages.Stage` instances

        """
        pipeline = [
            self.first_stage,
            QueryExistingArtifacts(),
            ArtifactDownloader(),
            DebDropEmptyContent(),
            ArtifactSaver(),
            DebUpdateReleaseFileAttributes(),
            DebUpdatePackageIndexAttributes(),
            QueryExistingContents(),
            ContentSaver(),
            RemoteArtifactSaver(),
            ResolveContentFutures(),
        ]
        return pipeline


def _filter_split(values, filter_list):
    """Filter space separated list and return iterable."""
    value_set = set(values.split())
    if filter_list:
        value_set &= set(filter_list)
    return sorted(value_set)


class DebUpdateReleaseFileAttributes(Stage):
    """
    This stage handles ReleaseFile content.

    It also transfers the sha256 from the artifact to the ReleaseFile content units.

    TODO: Verify signature
    """

    async def run(self):
        """
        Parse ReleaseFile content units.

        Update release content with information obtained from its artifact.
        """
        with ProgressReport(message="Update ReleaseFile units", code="update.release_file") as pb:
            async for d_content in self.items():
                if isinstance(d_content.content, ReleaseFile):
                    release_file = d_content.content
                    release_file_artifact = d_content.d_artifacts[0].artifact
                    release_file.sha256 = release_file_artifact.sha256
                    release_file_dict = deb822.Release(release_file_artifact.file)
                    release_file.codename = release_file_dict["Codename"]
                    release_file.suite = release_file_dict["Suite"]
                    # TODO split of extra stuff e.g. : 'updates/main' -> 'main'
                    release_file.components = release_file_dict["Components"]
                    release_file.architectures = release_file_dict["Architectures"]
                    log.debug("Codename: {}".format(release_file.codename))
                    log.debug("Components: {}".format(release_file.components))
                    log.debug("Architectures: {}".format(release_file.architectures))
                    pb.increment()
                await self.put(d_content)


class DebUpdatePackageIndexAttributes(Stage):  # TODO: Needs a new name
    """
    This stage handles PackageIndex content.
    """

    async def run(self):
        """
        Parse PackageIndex content units.

        Ensure, that an uncompressed artifact is available.
        """
        with ProgressReport(message="Update PackageIndex units", code="update.packageindex") as pb:
            async for d_content in self.items():
                if isinstance(d_content.content, PackageIndex):
                    if not d_content.d_artifacts:
                        raise NoPackageIndexFile()

                    content = d_content.content
                    if not [
                        da for da in d_content.d_artifacts if da.artifact.sha256 == content.sha256
                    ]:
                        # No main_artifact found uncompress one
                        filename = _uncompress_artifact(d_content.d_artifacts)
                        da = DeclarativeArtifact(
                            Artifact(sha256=content.sha256),
                            filename,
                            content.relative_path,
                            d_content.d_artifacts[0].remote,
                        )
                        d_content.d_artifacts.append(da)
                        await da.download()
                        da.artifact.save()
                        log.info(
                            "*** Expected: {} *** Uncompressed: {} ***".format(
                                content.sha256, da.artifact.sha256
                            )
                        )

                    pb.increment()
                await self.put(d_content)


def _uncompress_artifact(d_artifacts):
    for d_artifact in d_artifacts:
        ext = os.path.splitext(d_artifact.relative_path)[1]
        if ext == ".gz":
            compressor = gzip
        elif ext == ".bz2":
            compressor = bz2
        elif ext == ".xz":
            compressor = lzma
        else:
            log.info("Compression algorithm unknown for extension '{}'.".format(ext))
            continue
        # At this point we have found a file that can be decompressed
        with NamedTemporaryFile(delete=False) as f_out:
            with compressor.open(d_artifact.artifact.file) as f_in:
                shutil.copyfileobj(f_in, f_out)
        return "file://{}".format(f_out.name)
    # Not one artifact was suitable
    raise NoPackageIndexFile()


class DebDropEmptyContent(Stage):
    """
    This stage removes empty DeclarativeContent objects.

    In case we tried to fetch something, but the artifact 404ed, we simply drop it.
    """

    async def run(self):
        """
        Drop GenericContent units if they have no artifacts left.
        """
        async for d_content in self.items():
            d_content.d_artifacts = [
                d_artifact for d_artifact in d_content.d_artifacts if d_artifact.artifact
            ]
            if not d_content.d_artifacts:
                # No artifacts left -> drop it
                if d_content.future is not None:
                    d_content.future.set_result(None)
                continue
            await self.put(d_content)


class DebFirstStage(Stage):
    """
    The first stage of a pulp_deb sync pipeline.
    """

    def __init__(self, remote, *args, **kwargs):
        """
        The first stage of a pulp_deb sync pipeline.

        Args:
            remote (FileRemote): The remote data to be used when syncing

        """
        super().__init__(*args, **kwargs)
        self.remote = remote
        self.parsed_url = urlparse(remote.url)
        self.distributions = [
            distribution.strip() for distribution in self.remote.distributions.split()
        ]
        self.num_distributions = len(self.distributions)
        self.components = (
            None
            if self.remote.components is None
            else [component.strip() for component in self.remote.components.split()]
        )
        self.architectures = (
            None
            if self.remote.architectures is None
            else [architecture.strip() for architecture in self.remote.architectures.split()]
        )

    async def run(self):
        """
        Build and emit `DeclarativeContent` from the Release data.
        """
        # TODO Merge into one list of futures
        future_release_files = []
        future_package_indices = []
        future_installer_file_indices = []
        with ProgressReport(
            message="Creating download requests for Release files",
            code="download.release",
            total=self.num_distributions,
        ) as pb:
            for distribution in self.distributions:
                log.info('Downloading Release file for distribution: "{}"'.format(distribution))
                release_relpath = os.path.join("dists", distribution, "Release")
                release_path = os.path.join(self.parsed_url.path, release_relpath)
                release_da = DeclarativeArtifact(
                    Artifact(),
                    urlunparse(self.parsed_url._replace(path=release_path)),
                    release_relpath,
                    self.remote,
                    deferred_download=False,
                )
                release_gpg_relpath = os.path.join("dists", distribution, "Release.gpg")
                release_gpg_path = os.path.join(self.parsed_url.path, release_gpg_relpath)
                release_gpg_da = DeclarativeFailsafeArtifact(
                    Artifact(),
                    urlunparse(self.parsed_url._replace(path=release_gpg_path)),
                    release_gpg_relpath,
                    self.remote,
                    deferred_download=False,
                )
                inrelease_relpath = os.path.join("dists", distribution, "InRelease")
                inrelease_path = os.path.join(self.parsed_url.path, inrelease_relpath)
                inrelease_da = DeclarativeFailsafeArtifact(
                    Artifact(),
                    urlunparse(self.parsed_url._replace(path=inrelease_path)),
                    inrelease_relpath,
                    self.remote,
                    deferred_download=False,
                )
                release_file_unit = ReleaseFile(
                    distribution=distribution, relative_path=release_relpath
                )
                release_file_dc = DeclarativeContent(
                    content=release_file_unit,
                    d_artifacts=[release_da, release_gpg_da, inrelease_da],
                    does_batch=False,
                )
                future_release_files.append(release_file_dc.get_or_create_future())
                await self.put(release_file_dc)
                pb.increment()

        with ProgressReport(
            message="Parsing Release files",
            code="parsing.release_file",
            total=self.num_distributions,
        ) as pb:
            for release_file_future in asyncio.as_completed(future_release_files):
                release_file = await release_file_future
                if release_file is None:
                    continue
                log.info('Parsing Release file for release: "{}"'.format(release_file.codename))
                release_file_artifact = release_file._artifacts.get(sha256=release_file.sha256)
                release_file_dict = deb822.Release(release_file_artifact.file)
                async for d_content in self._read_release_file(release_file, release_file_dict):
                    if isinstance(d_content.content, PackageIndex):
                        future_package_indices.append(d_content.get_or_create_future())
                    if isinstance(d_content.content, InstallerFileIndex):
                        future_installer_file_indices.append(d_content.get_or_create_future())
                    await self.put(d_content)
                pb.increment()

        with ProgressReport(
            message="Parsing package index files", code="parsing.package_index"
        ) as pb:
            for package_index_future in asyncio.as_completed(future_package_indices):
                package_index = await package_index_future
                if package_index is None:
                    continue
                package_index_artifact = package_index.main_artifact
                log.debug(
                    "Parsing package index for {}:{}.".format(
                        package_index.component, package_index.architecture
                    )
                )
                async for package_dc in self._read_package_index(package_index_artifact.file):
                    await self.put(package_dc)
                pb.increment()

        with ProgressReport(
            message="Parsing installer file index files", code="parsing.installer_file_index"
        ) as pb:
            for installer_file_index_future in asyncio.as_completed(future_installer_file_indices):
                installer_file_index = await installer_file_index_future
                if installer_file_index is None:
                    continue
                log.debug(
                    "Parsing installer file index for {}:{}.".format(
                        installer_file_index.component, installer_file_index.architecture
                    )
                )
                async for d_content in self._read_installer_file_index(installer_file_index):
                    await self.put(d_content)
                pb.increment()

    async def _read_release_file(self, release_file, release_file_dict):
        """
        Parse a Release file of apt Repositories.

        Yield DeclarativeContent in the queue accordingly.

        Args:
            release_file_dict: parsed release file dictionary

        Returns:
            async iterator: Iterator of :class:`asyncio.Future` instances

        """

        def to_d_artifact(data):
            nonlocal release_file

            artifact = Artifact(**_get_checksums(data))
            relpath = os.path.join(os.path.dirname(release_file.relative_path), data["Name"])
            urlpath = os.path.join(self.parsed_url.path, relpath)
            return DeclarativeFailsafeArtifact(
                artifact,
                urlunparse(self.parsed_url._replace(path=urlpath)),
                relpath,
                self.remote,
                deferred_download=False,
            )

        def generate_source_index(component):
            raise NotImplementedError("Syncing source repositories is not yet implemented.")

        def generate_package_index(component, architecture, infix=""):
            nonlocal release_file
            nonlocal file_references

            package_index_dir = os.path.join(
                os.path.basename(component), infix, "binary-{}".format(architecture)
            )
            log.info("Downloading: {}/Packages".format(package_index_dir))
            d_artifacts = []
            for filename in ["Packages", "Packages.gz", "Packages.xz", "Release"]:
                path = os.path.join(package_index_dir, filename)
                if path in file_references:
                    d_artifacts.append(to_d_artifact(file_references.pop(path)))
            if not d_artifacts:
                return
            content_unit = PackageIndex(
                release=release_file,
                component=component,
                architecture=architecture,
                sha256=d_artifacts[0].artifact.sha256,
                relative_path=os.path.join(
                    os.path.dirname(release_file.relative_path), package_index_dir, "Packages"
                ),
            )
            d_content = DeclarativeContent(
                content=content_unit, d_artifacts=d_artifacts, does_batch=False
            )
            yield d_content

        def generate_installer_file_index(component, architecture):
            nonlocal release_file
            nonlocal file_references

            installer_file_index_dir = os.path.join(
                os.path.basename(component),
                "installer-{}".format(architecture),
                "current",
                "images",
            )
            log.info("Downloading installer files from {}".format(installer_file_index_dir))
            d_artifacts = []
            for filename in InstallerFileIndex.FILE_ALGORITHM.keys():
                path = os.path.join(installer_file_index_dir, filename)
                if path in file_references:
                    d_artifacts.append(to_d_artifact(file_references.pop(path)))
            if not d_artifacts:
                return
            content_unit = InstallerFileIndex(
                release=release_file,
                component=component,
                architecture=architecture,
                sha256=d_artifacts[0].artifact.sha256,
                relative_path=os.path.join(
                    os.path.dirname(release_file.relative_path), installer_file_index_dir
                ),
            )
            d_content = DeclarativeContent(
                content=content_unit, d_artifacts=d_artifacts, does_batch=False
            )
            yield d_content

        def generate_translation_files(component):
            nonlocal release_file
            nonlocal file_references

            translation_dir = os.path.join(os.path.basename(component), "i18n")
            paths = [path for path in file_references.keys() if path.startswith(translation_dir)]
            translations = {}
            for path in paths:
                d_artifact = to_d_artifact(file_references.pop(path))
                key, ext = os.path.splitext(path)
                if key not in translations:
                    translations[key] = {"sha256": None, "d_artifacts": []}
                if not ext:
                    translations[key]["sha256"] = d_artifact.artifact.sha256
                translations[key]["d_artifacts"].append(d_artifact)

            for path, translation in translations.items():
                content_unit = GenericContent(
                    sha256=translation["sha256"],
                    relative_path=os.path.join(os.path.dirname(release_file.relative_path), path),
                )
                d_content = DeclarativeContent(
                    content=content_unit, d_artifacts=translation["d_artifacts"]
                )
                yield d_content

        file_references = defaultdict(deb822.Deb822Dict)
        # collect file references in new dict
        for digest_name in ["SHA512", "SHA256", "SHA1", "MD5sum"]:
            if digest_name in release_file_dict:
                for unit in release_file_dict[digest_name]:
                    file_references[unit["Name"]].update(unit)
        # Find Package Index files for Component Architecture combinations
        for component in _filter_split(release_file.components, self.components):
            for architecture in _filter_split(release_file.architectures, self.architectures):
                log.info('Component: "{}" Architecture: "{}"'.format(component, architecture))
                for d_content in generate_package_index(component, architecture):
                    yield d_content
                if self.remote.sync_udebs:
                    for d_content in generate_package_index(
                        component, architecture, "debian-installer"
                    ):
                        yield d_content
                if self.remote.sync_installer:
                    for d_content in generate_installer_file_index(component, architecture):
                        yield d_content
            for d_content in generate_translation_files(component):
                yield d_content
            if self.remote.sync_sources:
                yield generate_source_index(component)

    async def _read_package_index(self, package_index):
        """
        Parse a package index file of apt Repositories.

        Put DeclarativeContent in the queue accordingly.

        Args:
            package_index: file object containing package paragraphs

        """
        # Interpret policy to download Artifacts or not
        deferred_download = self.remote.policy != Remote.IMMEDIATE

        for package_paragraph in deb822.Packages.iter_paragraphs(package_index):
            try:
                package_relpath = package_paragraph["Filename"]
                package_sha256 = package_paragraph["sha256"]
                if package_relpath.endswith(".deb"):
                    package_class = Package
                    serializer_class = Package822Serializer
                elif package_relpath.endswith(".udeb"):
                    package_class = InstallerPackage
                    serializer_class = InstallerPackage822Serializer
                log.debug("Downloading package {}".format(package_paragraph["Package"]))
                serializer = serializer_class.from822(data=package_paragraph)
                serializer.is_valid(raise_exception=True)
                package_content_unit = package_class(
                    relative_path=package_relpath,
                    sha256=package_sha256,
                    **serializer.validated_data,
                )
                package_path = os.path.join(self.parsed_url.path, package_relpath)
                package_artifact = Artifact(**_get_checksums(package_paragraph))
                package_da = DeclarativeArtifact(
                    artifact=package_artifact,
                    url=urlunparse(self.parsed_url._replace(path=package_path)),
                    relative_path=package_relpath,
                    remote=self.remote,
                    deferred_download=deferred_download,
                )
                package_dc = DeclarativeContent(
                    content=package_content_unit, d_artifacts=[package_da]
                )
                yield package_dc
            except KeyError:
                log.warning("Ignoring invalid package paragraph. {}".format(package_paragraph))

    async def _read_installer_file_index(self, installer_file_index):
        """
        Parse an installer file index file of apt Repositories.

        Put DeclarativeContent in the queue accordingly.

        Args:
            installer_file_index: object of type :class:`InstallerFileIndex`

        """
        # Interpret policy to download Artifacts or not
        deferred_download = self.remote.policy != Remote.IMMEDIATE

        file_list = defaultdict(dict)
        for content_artifact in installer_file_index.contentartifact_set.all():
            algorithm = InstallerFileIndex.FILE_ALGORITHM.get(
                os.path.basename(content_artifact.relative_path)
            )
            if not algorithm:
                continue
            for line in content_artifact.artifact.file:
                digest, filename = line.decode().strip().split(maxsplit=1)
                filename = os.path.normpath(filename)
                if filename in InstallerFileIndex.FILE_ALGORITHM:  # strangely they may appear here
                    continue
                file_list[filename][algorithm] = digest

        for filename, digests in file_list.items():
            relpath = os.path.join(installer_file_index.relative_path, filename)
            urlpath = os.path.join(self.parsed_url.path, relpath)
            content_unit = GenericContent(sha256=digests["sha256"], relative_path=relpath)
            d_artifact = DeclarativeArtifact(
                artifact=Artifact(**digests),
                url=urlunparse(self.parsed_url._replace(path=urlpath)),
                relative_path=relpath,
                remote=self.remote,
                deferred_download=deferred_download,
            )
            d_content = DeclarativeContent(content=content_unit, d_artifacts=[d_artifact])
            yield d_content


def _get_checksums(unit_dict):
    return {
        k: unit_dict[v]
        for k, v in {
            "sha512": "SHA512",
            "sha256": "SHA256",
            "sha1": "SHA1",
            "md5": "MD5sum",
        }.items()
        if v in unit_dict
    }
