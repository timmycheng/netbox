import django_tables2 as tables
from django_tables2.utils import Accessor
from django.utils.translation import gettext_lazy as _
from netbox.tables import NetBoxTable, columns
from tenancy.tables import TenancyColumnsMixin
from .models import ApplicationGroup, Application, ApplicationServer, ApplicationEndpoint, ApplicationPersonnel


class ApplicationGroupTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    application_count = columns.LinkedCountColumn(
        viewname='appm:application_list',
        url_params={'group_id': 'pk'},
        verbose_name=_('Applications')
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = ApplicationGroup
        fields = (
            'pk', 'id', 'name', 'slug', 'application_count', 'description',
            'created', 'last_updated', 'actions'
        )
        default_columns = ('pk', 'name', 'application_count', 'description')


class ApplicationTable(TenancyColumnsMixin, NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    group = tables.Column(
        linkify=True
    )
    status = columns.ChoiceFieldColumn()
    criticality = columns.ChoiceFieldColumn()
    environment = columns.ChoiceFieldColumn()
    server_count = columns.LinkedCountColumn(
        viewname='appm:applicationserver_list',
        url_params={'application_id': 'pk'},
        verbose_name=_('Servers')
    )
    endpoint_count = columns.LinkedCountColumn(
        viewname='appm:applicationendpoint_list',
        url_params={'application_id': 'pk'},
        verbose_name=_('Endpoints')
    )
    personnel_count = columns.LinkedCountColumn(
        viewname='appm:applicationpersonnel_list',
        url_params={'application_id': 'pk'},
        verbose_name=_('Personnel')
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = Application
        fields = (
            'pk', 'id', 'name', 'slug', 'group', 'status', 'version', 'owner',
            'business_unit', 'criticality', 'environment', 'tenant', 'server_count',
            'endpoint_count', 'personnel_count', 'description', 'created',
            'last_updated', 'actions'
        )
        default_columns = (
            'pk', 'name', 'group', 'status', 'environment', 'server_count',
            'endpoint_count', 'personnel_count'
        )


class ApplicationServerTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    application = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )
    virtual_machine = tables.Column(
        linkify=True
    )
    role = columns.ChoiceFieldColumn()
    status = columns.ChoiceFieldColumn()
    cpu_cores = tables.Column(
        verbose_name=_('CPU Cores')
    )
    memory_gb = tables.Column(
        verbose_name=_('Memory (GB)')
    )
    storage_gb = tables.Column(
        verbose_name=_('Storage (GB)')
    )
    endpoint_count = columns.LinkedCountColumn(
        viewname='appm:applicationendpoint_list',
        url_params={'server_id': 'pk'},
        verbose_name=_('Endpoints')
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = ApplicationServer
        fields = (
            'pk', 'id', 'name', 'application', 'device', 'virtual_machine',
            'role', 'status', 'cpu_cores', 'memory_gb', 'storage_gb',
            'operating_system', 'endpoint_count', 'description', 'created',
            'last_updated', 'actions'
        )
        default_columns = (
            'pk', 'name', 'application', 'device', 'virtual_machine', 'role',
            'status', 'endpoint_count'
        )


class ApplicationEndpointTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    application = tables.Column(
        linkify=True
    )
    server = tables.Column(
        linkify=True
    )
    type = columns.ChoiceFieldColumn()
    status = columns.ChoiceFieldColumn()
    url = tables.URLColumn(
        verbose_name=_('URL')
    )
    ip_address = tables.Column(
        verbose_name=_('IP Address')
    )
    port = tables.Column()
    protocol = tables.Column()
    is_public = columns.BooleanColumn(
        verbose_name=_('Public')
    )
    is_load_balanced = columns.BooleanColumn(
        verbose_name=_('Load Balanced')
    )
    ssl_enabled = columns.BooleanColumn(
        verbose_name=_('SSL')
    )
    authentication_required = columns.BooleanColumn(
        verbose_name=_('Auth Required')
    )
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = ApplicationEndpoint
        fields = (
            'pk', 'id', 'name', 'application', 'server', 'type', 'status',
            'url', 'ip_address', 'port', 'protocol', 'path', 'is_public',
            'is_load_balanced', 'ssl_enabled', 'authentication_required',
            'health_check_url', 'documentation_url', 'description', 'created',
            'last_updated', 'actions'
        )
        default_columns = (
            'pk', 'name', 'application', 'server', 'type', 'status', 'url',
            'port', 'is_public', 'ssl_enabled'
        )


class ApplicationPersonnelTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    application = tables.Column(
        linkify=True
    )
    contact = tables.Column(
        linkify=True
    )
    role = columns.ChoiceFieldColumn()
    email = tables.EmailColumn()
    phone = tables.Column()
    department = tables.Column()
    title = tables.Column()
    is_primary = columns.BooleanColumn(
        verbose_name=_('Primary')
    )
    is_emergency_contact = columns.BooleanColumn(
        verbose_name=_('Emergency Contact')
    )
    start_date = tables.DateColumn()
    end_date = tables.DateColumn()
    actions = columns.ActionsColumn()

    class Meta(NetBoxTable.Meta):
        model = ApplicationPersonnel
        fields = (
            'pk', 'id', 'name', 'application', 'contact', 'role', 'email',
            'phone', 'department', 'title', 'is_primary', 'is_emergency_contact',
            'start_date', 'end_date', 'notes', 'created', 'last_updated', 'actions'
        )
        default_columns = (
            'pk', 'name', 'application', 'role', 'email', 'phone', 'is_primary',
            'is_emergency_contact'
        )