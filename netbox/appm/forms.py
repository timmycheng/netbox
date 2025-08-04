from django import forms
from django.core.exceptions import ValidationError
from netbox.forms import NetBoxModelForm, NetBoxModelImportForm, NetBoxModelBulkEditForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField, SlugField
from utilities.forms.rendering import FieldSet
from utilities.forms.utils import add_blank_choice
from utilities.forms.widgets import BulkEditNullBooleanSelect
from tenancy.forms import TenancyForm
from dcim.models import Device
from virtualization.models import VirtualMachine
from tenancy.models import Contact
from .models import ApplicationGroup, Application, ApplicationServer, ApplicationEndpoint, ApplicationPersonnel
from .choices import (
    ApplicationStatusChoices, ApplicationCriticalityChoices, ApplicationEnvironmentChoices,
    ServerStatusChoices, ServerRoleChoices, EndpointStatusChoices, EndpointTypeChoices,
    PersonnelRoleChoices
)


class ApplicationGroupForm(NetBoxModelForm):
    parent = DynamicModelChoiceField(
        queryset=ApplicationGroup.objects.all(),
        required=False
    )
    slug = SlugField()

    fieldsets = (
        FieldSet('parent', 'name', 'slug', 'description', name='Application Group'),
    )

    class Meta:
        model = ApplicationGroup
        fields = ('parent', 'name', 'slug', 'description')


class ApplicationForm(TenancyForm, NetBoxModelForm):
    group = DynamicModelChoiceField(
        queryset=ApplicationGroup.objects.all(),
        required=False
    )
    slug = SlugField()
    status = forms.ChoiceField(
        choices=add_blank_choice(ApplicationStatusChoices),
        required=False
    )
    criticality = forms.ChoiceField(
        choices=add_blank_choice(ApplicationCriticalityChoices),
        required=False
    )
    environment = forms.ChoiceField(
        choices=add_blank_choice(ApplicationEnvironmentChoices),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('group', 'name', 'slug', 'status', 'version', name='Application'),
        FieldSet('owner', 'business_unit', 'criticality', 'environment', name='Organization'),
        FieldSet('tenant_group', 'tenant', name='Tenancy'),
        FieldSet('description', name='Details'),
    )

    class Meta:
        model = Application
        fields = (
            'group', 'name', 'slug', 'status', 'version', 'owner', 'business_unit',
            'criticality', 'environment', 'tenant', 'description', 'comments'
        )


class ApplicationServerForm(NetBoxModelForm):
    application = DynamicModelChoiceField(
        queryset=Application.objects.all()
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False
    )
    role = forms.ChoiceField(
        choices=add_blank_choice(ServerRoleChoices),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(ServerStatusChoices),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('application', 'name', 'role', 'status', name='Server'),
        FieldSet('device', 'virtual_machine', name='Infrastructure'),
        FieldSet('cpu_cores', 'memory_gb', 'storage_gb', 'operating_system', name='Specifications'),
        FieldSet('middleware', name='Software'),
        FieldSet('description', name='Details'),
    )

    class Meta:
        model = ApplicationServer
        fields = (
            'application', 'name', 'role', 'status', 'device', 'virtual_machine',
            'cpu_cores', 'memory_gb', 'storage_gb', 'operating_system', 'middleware',
            'description', 'comments'
        )

    def clean(self):
        cleaned_data = super().clean()
        device = cleaned_data.get('device')
        virtual_machine = cleaned_data.get('virtual_machine')

        if device and virtual_machine:
            raise ValidationError('A server cannot be associated with both a device and a virtual machine.')
        if not device and not virtual_machine:
            raise ValidationError('A server must be associated with either a device or a virtual machine.')

        return cleaned_data


class ApplicationEndpointForm(NetBoxModelForm):
    application = DynamicModelChoiceField(
        queryset=Application.objects.all()
    )
    server = DynamicModelChoiceField(
        queryset=ApplicationServer.objects.all(),
        required=False,
        query_params={
            'application': '$application'
        }
    )
    type = forms.ChoiceField(
        choices=add_blank_choice(EndpointTypeChoices),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(EndpointStatusChoices),
        required=False
    )
    comments = CommentField()

    fieldsets = (
        FieldSet('application', 'server', 'name', 'type', 'status', name='Endpoint'),
        FieldSet('url', 'ip_address', 'port', 'protocol', 'path', name='Network'),
        FieldSet('is_public', 'is_load_balanced', 'authentication_required', 'ssl_enabled', name='Configuration'),
        FieldSet('health_check_url', 'documentation_url', name='Monitoring'),
        FieldSet('description', name='Details'),
    )

    class Meta:
        model = ApplicationEndpoint
        fields = (
            'application', 'server', 'name', 'type', 'status', 'url', 'ip_address',
            'port', 'protocol', 'path', 'is_public', 'is_load_balanced',
            'health_check_url', 'authentication_required', 'ssl_enabled',
            'documentation_url', 'description', 'comments'
        )


class ApplicationPersonnelForm(NetBoxModelForm):
    application = DynamicModelChoiceField(
        queryset=Application.objects.all()
    )
    contact = DynamicModelChoiceField(
        queryset=Contact.objects.all(),
        required=False
    )
    role = forms.ChoiceField(
        choices=add_blank_choice(PersonnelRoleChoices),
        required=False
    )

    fieldsets = (
        FieldSet('application', 'contact', 'name', 'role', name='Personnel'),
        FieldSet('email', 'phone', 'department', 'title', name='Contact Information'),
        FieldSet('is_primary', 'is_emergency_contact', 'start_date', 'end_date', name='Status'),
        FieldSet('notes', name='Notes'),
    )

    class Meta:
        model = ApplicationPersonnel
        fields = (
            'application', 'contact', 'name', 'role', 'email', 'phone',
            'department', 'title', 'is_primary', 'is_emergency_contact',
            'start_date', 'end_date', 'notes'
        )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError('End date cannot be earlier than start date.')

        return cleaned_data


# Import Forms
class ApplicationGroupImportForm(NetBoxModelImportForm):
    parent = forms.ModelChoiceField(
        queryset=ApplicationGroup.objects.all(),
        to_field_name='name',
        required=False
    )

    class Meta:
        model = ApplicationGroup
        fields = ('parent', 'name', 'slug', 'description')


class ApplicationImportForm(NetBoxModelImportForm):
    group = forms.ModelChoiceField(
        queryset=ApplicationGroup.objects.all(),
        to_field_name='name',
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(ApplicationStatusChoices),
        required=False
    )
    criticality = forms.ChoiceField(
        choices=add_blank_choice(ApplicationCriticalityChoices),
        required=False
    )
    environment = forms.ChoiceField(
        choices=add_blank_choice(ApplicationEnvironmentChoices),
        required=False
    )

    class Meta:
        model = Application
        fields = (
            'group', 'name', 'slug', 'status', 'version', 'owner', 'business_unit',
            'criticality', 'environment', 'tenant', 'description', 'comments'
        )


class ApplicationServerImportForm(NetBoxModelImportForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.all(),
        to_field_name='name'
    )
    device = forms.ModelChoiceField(
        queryset=Device.objects.all(),
        to_field_name='name',
        required=False
    )
    virtual_machine = forms.ModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        required=False
    )
    role = forms.ChoiceField(
        choices=add_blank_choice(ServerRoleChoices),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(ServerStatusChoices),
        required=False
    )

    class Meta:
        model = ApplicationServer
        fields = (
            'application', 'name', 'role', 'status', 'device', 'virtual_machine',
            'cpu_cores', 'memory_gb', 'storage_gb', 'operating_system', 'middleware',
            'description', 'comments'
        )


class ApplicationEndpointImportForm(NetBoxModelImportForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.all(),
        to_field_name='name'
    )
    server = forms.ModelChoiceField(
        queryset=ApplicationServer.objects.all(),
        to_field_name='name',
        required=False
    )
    type = forms.ChoiceField(
        choices=add_blank_choice(EndpointTypeChoices),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(EndpointStatusChoices),
        required=False
    )

    class Meta:
        model = ApplicationEndpoint
        fields = (
            'application', 'server', 'name', 'type', 'status', 'url', 'ip_address',
            'port', 'protocol', 'path', 'is_public', 'is_load_balanced',
            'health_check_url', 'authentication_required', 'ssl_enabled',
            'documentation_url', 'description', 'comments'
        )


class ApplicationPersonnelImportForm(NetBoxModelImportForm):
    application = forms.ModelChoiceField(
        queryset=Application.objects.all(),
        to_field_name='name'
    )
    contact = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        to_field_name='name',
        required=False
    )
    role = forms.ChoiceField(
        choices=add_blank_choice(PersonnelRoleChoices),
        required=False
    )

    class Meta:
        model = ApplicationPersonnel
        fields = (
            'application', 'contact', 'name', 'role', 'email', 'phone',
            'department', 'title', 'is_primary', 'is_emergency_contact',
            'start_date', 'end_date', 'notes'
        )


# Bulk Edit Forms
class ApplicationGroupBulkEditForm(NetBoxModelBulkEditForm):
    parent = DynamicModelChoiceField(
        queryset=ApplicationGroup.objects.all(),
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )

    model = ApplicationGroup
    fieldsets = (
        FieldSet('parent', 'description'),
    )
    nullable_fields = ('parent', 'description')


class ApplicationBulkEditForm(NetBoxModelBulkEditForm):
    group = DynamicModelChoiceField(
        queryset=ApplicationGroup.objects.all(),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(ApplicationStatusChoices),
        required=False
    )
    criticality = forms.ChoiceField(
        choices=add_blank_choice(ApplicationCriticalityChoices),
        required=False
    )
    environment = forms.ChoiceField(
        choices=add_blank_choice(ApplicationEnvironmentChoices),
        required=False
    )
    version = forms.CharField(
        max_length=50,
        required=False
    )
    owner = forms.CharField(
        max_length=100,
        required=False
    )
    business_unit = forms.CharField(
        max_length=100,
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = Application
    fieldsets = (
        FieldSet('group', 'status', 'criticality', 'environment', 'version', 'owner', 'business_unit'),
        FieldSet('description', name='Details'),
    )
    nullable_fields = (
        'group', 'status', 'criticality', 'environment', 'version', 'owner',
        'business_unit', 'description', 'comments'
    )


class ApplicationServerBulkEditForm(NetBoxModelBulkEditForm):
    application = DynamicModelChoiceField(
        queryset=Application.objects.all(),
        required=False
    )
    role = forms.ChoiceField(
        choices=add_blank_choice(ServerRoleChoices),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(ServerStatusChoices),
        required=False
    )
    cpu_cores = forms.IntegerField(
        required=False
    )
    memory_gb = forms.IntegerField(
        required=False
    )
    storage_gb = forms.IntegerField(
        required=False
    )
    operating_system = forms.CharField(
        max_length=100,
        required=False
    )
    description = forms.CharField(
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = ApplicationServer
    fieldsets = (
        FieldSet('application', 'role', 'status', 'cpu_cores', 'memory_gb', 'storage_gb', 'operating_system'),
        FieldSet('description', name='Details'),
    )
    nullable_fields = (
        'application', 'role', 'status', 'cpu_cores', 'memory_gb', 'storage_gb',
        'operating_system', 'description', 'comments'
    )


class ApplicationEndpointBulkEditForm(NetBoxModelBulkEditForm):
    application = DynamicModelChoiceField(
        queryset=Application.objects.all(),
        required=False
    )
    type = forms.ChoiceField(
        choices=add_blank_choice(EndpointTypeChoices),
        required=False
    )
    status = forms.ChoiceField(
        choices=add_blank_choice(EndpointStatusChoices),
        required=False
    )
    protocol = forms.CharField(
        max_length=20,
        required=False
    )
    is_public = BulkEditNullBooleanSelect()
    is_load_balanced = BulkEditNullBooleanSelect()
    authentication_required = BulkEditNullBooleanSelect()
    ssl_enabled = BulkEditNullBooleanSelect()
    description = forms.CharField(
        max_length=200,
        required=False
    )
    comments = CommentField()

    model = ApplicationEndpoint
    fieldsets = (
        FieldSet('application', 'type', 'status', 'protocol'),
        FieldSet('is_public', 'is_load_balanced', 'authentication_required', 'ssl_enabled', name='Configuration'),
        FieldSet('description', name='Details'),
    )
    nullable_fields = (
        'application', 'type', 'status', 'protocol', 'description', 'comments'
    )


class ApplicationPersonnelBulkEditForm(NetBoxModelBulkEditForm):
    application = DynamicModelChoiceField(
        queryset=Application.objects.all(),
        required=False
    )
    role = forms.ChoiceField(
        choices=add_blank_choice(PersonnelRoleChoices),
        required=False
    )
    department = forms.CharField(
        max_length=100,
        required=False
    )
    title = forms.CharField(
        max_length=100,
        required=False
    )
    is_primary = BulkEditNullBooleanSelect()
    is_emergency_contact = BulkEditNullBooleanSelect()

    model = ApplicationPersonnel
    fieldsets = (
        FieldSet('application', 'role', 'department', 'title'),
        FieldSet('is_primary', 'is_emergency_contact', name='Status'),
    )
    nullable_fields = ('application', 'role', 'department', 'title')
