from netbox.api.viewsets import NetBoxModelViewSet
from ..models import ApplicationGroup, Application, ApplicationServer, ApplicationEndpoint, ApplicationPersonnel
from .serializers import (
    ApplicationGroupSerializer, ApplicationSerializer, ApplicationServerSerializer,
    ApplicationEndpointSerializer, ApplicationPersonnelSerializer
)
from ..filtersets import (
    ApplicationGroupFilterSet, ApplicationFilterSet, ApplicationServerFilterSet,
    ApplicationEndpointFilterSet, ApplicationPersonnelFilterSet
)


class ApplicationGroupViewSet(NetBoxModelViewSet):
    queryset = ApplicationGroup.objects.prefetch_related('tags')
    serializer_class = ApplicationGroupSerializer
    filterset_class = ApplicationGroupFilterSet


class ApplicationViewSet(NetBoxModelViewSet):
    queryset = Application.objects.prefetch_related(
        'group', 'tenant', 'tags'
    )
    serializer_class = ApplicationSerializer
    filterset_class = ApplicationFilterSet


class ApplicationServerViewSet(NetBoxModelViewSet):
    queryset = ApplicationServer.objects.prefetch_related(
        'application', 'device', 'virtual_machine', 'tags'
    )
    serializer_class = ApplicationServerSerializer
    filterset_class = ApplicationServerFilterSet


class ApplicationEndpointViewSet(NetBoxModelViewSet):
    queryset = ApplicationEndpoint.objects.prefetch_related(
        'application', 'server', 'tags'
    )
    serializer_class = ApplicationEndpointSerializer
    filterset_class = ApplicationEndpointFilterSet


class ApplicationPersonnelViewSet(NetBoxModelViewSet):
    queryset = ApplicationPersonnel.objects.prefetch_related(
        'application', 'contact', 'tags'
    )
    serializer_class = ApplicationPersonnelSerializer
    filterset_class = ApplicationPersonnelFilterSet