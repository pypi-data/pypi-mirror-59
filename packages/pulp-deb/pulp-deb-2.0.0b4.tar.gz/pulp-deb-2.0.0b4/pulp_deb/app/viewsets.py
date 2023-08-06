from gettext import gettext as _  # noqa

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action

from pulpcore.plugin.actions import ModifyRepositoryActionMixin
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import enqueue_with_reservation
from pulpcore.plugin.viewsets import (
    BaseDistributionViewSet,
    ContentViewSet,
    ContentFilter,
    RemoteViewSet,
    OperationPostponedResponse,
    PublicationViewSet,
    RepositoryVersionViewSet,
    RepositoryViewSet,
    SingleArtifactContentUploadViewSet,
)

from . import models, serializers, tasks


# Content


class GenericContentFilter(ContentFilter):
    """
    FilterSet for GenericContent.
    """

    class Meta:
        model = models.GenericContent
        fields = ["relative_path", "sha256"]


class GenericContentViewSet(SingleArtifactContentUploadViewSet):
    """
    A ViewSet for GenericContent.
    """

    endpoint_name = "generic_contents"
    queryset = models.GenericContent.objects.prefetch_related("_artifacts")
    serializer_class = serializers.GenericContentSerializer
    filterset_class = GenericContentFilter


class PackageFilter(ContentFilter):
    """
    FilterSet for Package.
    """

    class Meta:
        model = models.Package
        fields = [
            "package",
            "source",
            "version",
            "architecture",
            "section",
            "priority",
            "origin",
            "tag",
            "essential",
            "build_essential",
            "installed_size",
            "maintainer",
            "original_maintainer",
            "built_using",
            "auto_built_package",
            "multi_arch",
            "sha256",
            "relative_path",
        ]


class PackageViewSet(SingleArtifactContentUploadViewSet):
    """
    A ViewSet for Package.
    """

    endpoint_name = "packages"
    queryset = models.Package.objects.prefetch_related("_artifacts")
    serializer_class = serializers.PackageSerializer
    filterset_class = PackageFilter


class InstallerPackageFilter(ContentFilter):
    """
    FilterSet for InstallerPackage.
    """

    class Meta:
        model = models.InstallerPackage
        fields = [
            "package",
            "source",
            "version",
            "architecture",
            "section",
            "priority",
            "origin",
            "tag",
            "essential",
            "build_essential",
            "installed_size",
            "maintainer",
            "original_maintainer",
            "built_using",
            "auto_built_package",
            "multi_arch",
            "sha256",
        ]


class InstallerPackageViewSet(SingleArtifactContentUploadViewSet):
    """
    A ViewSet for InstallerPackage.
    """

    endpoint_name = "installer_packages"
    queryset = models.InstallerPackage.objects.prefetch_related("_artifacts")
    serializer_class = serializers.InstallerPackageSerializer
    filterset_class = InstallerPackageFilter


# Metadata


class ReleaseFileFilter(ContentFilter):
    """
    FilterSet for ReleaseFile.
    """

    class Meta:
        model = models.ReleaseFile
        fields = ["codename", "suite", "relative_path", "sha256"]


class ReleaseFileViewSet(ContentViewSet):
    """
    A ViewSet for ReleaseFile.
    """

    endpoint_name = "release_files"
    queryset = models.ReleaseFile.objects.all()
    serializer_class = serializers.ReleaseFileSerializer
    filterset_class = ReleaseFileFilter


class PackageIndexFilter(ContentFilter):
    """
    FilterSet for PackageIndex.
    """

    class Meta:
        model = models.PackageIndex
        fields = ["component", "architecture", "relative_path", "sha256"]


class PackageIndexViewSet(ContentViewSet):
    """
    A ViewSet for PackageIndex.
    """

    endpoint_name = "package_index"
    queryset = models.PackageIndex.objects.all()
    serializer_class = serializers.PackageIndexSerializer
    filterset_class = PackageIndexFilter


class InstallerFileIndexFilter(ContentFilter):
    """
    FilterSet for InstallerFileIndex.
    """

    class Meta:
        model = models.InstallerFileIndex
        fields = ["component", "architecture", "relative_path", "sha256"]


class InstallerFileIndexViewSet(ContentViewSet):
    """
    A ViewSet for InstallerFileIndex.
    """

    endpoint_name = "installer_file_index"
    queryset = models.InstallerFileIndex.objects.all()
    serializer_class = serializers.InstallerFileIndexSerializer
    filterset_class = InstallerFileIndexFilter


# Infrastructure


class DebRemoteViewSet(RemoteViewSet):
    """
    A ViewSet for DebRemote.
    """

    endpoint_name = "apt"
    queryset = models.DebRemote.objects.all()
    serializer_class = serializers.DebRemoteSerializer


class DebRepositoryViewSet(RepositoryViewSet, ModifyRepositoryActionMixin):
    """
    A ViewSet for DebRepository.
    """

    endpoint_name = "apt"
    queryset = models.DebRepository.objects.all()
    serializer_class = serializers.DebRepositorySerializer

    # This decorator is necessary since a sync operation is asyncrounous and returns
    # the id and href of the sync task.
    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to sync content",
        operation_summary="Sync from remote",
        responses={202: AsyncOperationResponseSerializer},
    )
    @action(detail=True, methods=["post"], serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Dispatches a sync task.
        """
        repository = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={"request": request})

        # Validate synchronously to return 400 errors.
        serializer.is_valid(raise_exception=True)
        remote = serializer.validated_data.get("remote")
        mirror = serializer.validated_data.get("mirror", True)

        result = enqueue_with_reservation(
            tasks.synchronize,
            [repository, remote],
            kwargs={"remote_pk": remote.pk, "repository_pk": repository.pk, "mirror": mirror},
        )
        return OperationPostponedResponse(result, request)


class DebRepositoryVersionViewSet(RepositoryVersionViewSet):
    """
    DebRepositoryVersion represents a single deb repository version.
    """

    parent_viewset = DebRepositoryViewSet


class VerbatimPublicationViewSet(PublicationViewSet):
    """
    A ViewSet for VerbatimPublication.
    """

    endpoint_name = "verbatim"
    queryset = models.VerbatimPublication.objects.exclude(complete=False)
    serializer_class = serializers.VerbatimPublicationSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get("repository_version")

        result = enqueue_with_reservation(
            tasks.publish_verbatim,
            [repository_version.repository],
            kwargs={"repository_version_pk": str(repository_version.pk)},
        )
        return OperationPostponedResponse(result, request)


class DebPublicationViewSet(PublicationViewSet):
    """
    A ViewSet for DebPublication.
    """

    endpoint_name = "apt"
    queryset = models.DebPublication.objects.exclude(complete=False)
    serializer_class = serializers.DebPublicationSerializer

    @swagger_auto_schema(
        operation_description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get("repository_version")
        simple = serializer.validated_data.get("simple")
        structured = serializer.validated_data.get("structured")

        result = enqueue_with_reservation(
            tasks.publish,
            [repository_version.repository],
            kwargs={
                "repository_version_pk": str(repository_version.pk),
                "simple": simple,
                "structured": structured,
            },
        )
        return OperationPostponedResponse(result, request)


class DebDistributionViewSet(BaseDistributionViewSet):
    """
    ViewSet for DebDistributions.
    """

    endpoint_name = "apt"
    queryset = models.DebDistribution.objects.all()
    serializer_class = serializers.DebDistributionSerializer
