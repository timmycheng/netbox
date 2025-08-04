from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from tenancy.api.serializers import TenantSerializer
from dcim.api.serializers import DeviceSerializer
from virtualization.api.serializers import VirtualMachineSerializer
from tenancy.api.serializers import ContactSerializer
from ..models import ApplicationGroup, Application, ApplicationServer, ApplicationEndpoint, ApplicationPersonnel


class ApplicationGroupSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='appm-api:applicationgroup-detail'
    )
    application_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ApplicationGroup
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'description',
            'application_count', 'created', 'last_updated', 'custom_fields'
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'slug')


class ApplicationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='appm-api:application-detail'
    )
    group = ApplicationGroupSerializer(read_only=True)
    tenant = TenantSerializer(read_only=True)
    server_count = serializers.IntegerField(read_only=True)
    endpoint_count = serializers.IntegerField(read_only=True)
    personnel_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'url', 'display', 'name', 'slug', 'group', 'status', 'version',
            'owner', 'business_unit', 'criticality', 'environment', 'tenant',
            'description', 'comments', 'server_count', 'endpoint_count',
            'personnel_count', 'created', 'last_updated', 'custom_fields', 'tags'
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'slug')


class ApplicationServerSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='appm-api:applicationserver-detail'
    )
    application = ApplicationSerializer(read_only=True)
    device = DeviceSerializer(read_only=True)
    virtual_machine = VirtualMachineSerializer(read_only=True)
    endpoint_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ApplicationServer
        fields = [
            'id', 'url', 'display', 'name', 'application', 'device', 'virtual_machine',
            'role', 'status', 'cpu_cores', 'memory_gb', 'storage_gb',
            'operating_system', 'middleware', 'description', 'comments',
            'endpoint_count', 'created', 'last_updated', 'custom_fields', 'tags'
        ]
        brief_fields = ('id', 'url', 'display', 'name')


class ApplicationEndpointSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='appm-api:applicationendpoint-detail'
    )
    application = ApplicationSerializer(read_only=True)
    server = ApplicationServerSerializer(read_only=True)

    class Meta:
        model = ApplicationEndpoint
        fields = [
            'id', 'url', 'display', 'name', 'application', 'server', 'type',
            'status', 'url_field', 'ip_address', 'port', 'protocol', 'path',
            'is_public', 'is_load_balanced', 'health_check_url',
            'authentication_required', 'ssl_enabled', 'documentation_url',
            'description', 'comments', 'created', 'last_updated',
            'custom_fields', 'tags'
        ]
        brief_fields = ('id', 'url', 'display', 'name')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Rename 'url_field' to 'url' in the output to avoid conflict with DRF's url field
        if 'url_field' in data:
            data['endpoint_url'] = data.pop('url_field')
        return data


class ApplicationPersonnelSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='appm-api:applicationpersonnel-detail'
    )
    application = ApplicationSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = ApplicationPersonnel
        fields = [
            'id', 'url', 'display', 'name', 'application', 'contact', 'role',
            'email', 'phone', 'department', 'title', 'is_primary',
            'is_emergency_contact', 'start_date', 'end_date', 'notes',
            'created', 'last_updated', 'custom_fields', 'tags'
        ]
        brief_fields = ('id', 'url', 'display', 'name', 'role')