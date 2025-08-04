import django_filters
from django.db.models import Q
from netbox.filtersets import NetBoxModelFilterSet
from utilities.filters import TreeNodeMultipleChoiceFilter, MultiValueCharFilter
from tenancy.filtersets import TenancyFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from tenancy.models import Contact
from .models import ApplicationGroup, Application, ApplicationServer, ApplicationEndpoint, ApplicationPersonnel
from .choices import (
    ApplicationStatusChoices, ApplicationCriticalityChoices, ApplicationEnvironmentChoices,
    ServerStatusChoices, ServerRoleChoices, EndpointStatusChoices, EndpointTypeChoices,
    PersonnelRoleChoices
)


class ApplicationGroupFilterSet(NetBoxModelFilterSet):
    pass

    class Meta:
        model = ApplicationGroup
        fields = ('id', 'name', 'slug', 'description')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value)
        )


class ApplicationFilterSet(TenancyFilterSet, NetBoxModelFilterSet):
    group_id = TreeNodeMultipleChoiceFilter(
        queryset=ApplicationGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        label='Application group (ID)',
    )
    group = TreeNodeMultipleChoiceFilter(
        queryset=ApplicationGroup.objects.all(),
        field_name='group',
        lookup_expr='in',
        to_field_name='slug',
        label='Application group (slug)',
    )
    status = django_filters.MultipleChoiceFilter(
        choices=ApplicationStatusChoices,
        null_value=None,
    )
    criticality = django_filters.MultipleChoiceFilter(
        choices=ApplicationCriticalityChoices,
        null_value=None,
    )
    environment = django_filters.MultipleChoiceFilter(
        choices=ApplicationEnvironmentChoices,
        null_value=None,
    )
    owner = MultiValueCharFilter(
        lookup_expr='icontains'
    )
    business_unit = MultiValueCharFilter(
        lookup_expr='icontains'
    )
    version = MultiValueCharFilter(
        lookup_expr='icontains'
    )

    class Meta:
        model = Application
        fields = ('id', 'name', 'slug', 'description', 'comments')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(slug__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value) |
            Q(owner__icontains=value) |
            Q(business_unit__icontains=value) |
            Q(version__icontains=value)
        )


class ApplicationServerFilterSet(NetBoxModelFilterSet):
    application_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Application.objects.all(),
        label='Application (ID)',
    )
    application = django_filters.ModelMultipleChoiceFilter(
        field_name='application__slug',
        queryset=Application.objects.all(),
        to_field_name='slug',
        label='Application (slug)',
    )
    device_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Device.objects.all(),
        label='Device (ID)',
    )
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__name',
        queryset=Device.objects.all(),
        to_field_name='name',
        label='Device (name)',
    )
    virtual_machine_id = django_filters.ModelMultipleChoiceFilter(
        queryset=VirtualMachine.objects.all(),
        label='Virtual machine (ID)',
    )
    virtual_machine = django_filters.ModelMultipleChoiceFilter(
        field_name='virtual_machine__name',
        queryset=VirtualMachine.objects.all(),
        to_field_name='name',
        label='Virtual machine (name)',
    )
    role = django_filters.MultipleChoiceFilter(
        choices=ServerRoleChoices,
        null_value=None,
    )
    status = django_filters.MultipleChoiceFilter(
        choices=ServerStatusChoices,
        null_value=None,
    )
    operating_system = MultiValueCharFilter(
        lookup_expr='icontains'
    )

    class Meta:
        model = ApplicationServer
        fields = ('id', 'name', 'description', 'comments')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value) |
            Q(operating_system__icontains=value) |
            Q(middleware__icontains=value)
        )


class ApplicationEndpointFilterSet(NetBoxModelFilterSet):
    application_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Application.objects.all(),
        label='Application (ID)',
    )
    application = django_filters.ModelMultipleChoiceFilter(
        field_name='application__slug',
        queryset=Application.objects.all(),
        to_field_name='slug',
        label='Application (slug)',
    )
    server_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ApplicationServer.objects.all(),
        label='Server (ID)',
    )
    server = django_filters.ModelMultipleChoiceFilter(
        field_name='server__name',
        queryset=ApplicationServer.objects.all(),
        to_field_name='name',
        label='Server (name)',
    )
    type = django_filters.MultipleChoiceFilter(
        choices=EndpointTypeChoices,
        null_value=None,
    )
    status = django_filters.MultipleChoiceFilter(
        choices=EndpointStatusChoices,
        null_value=None,
    )
    protocol = MultiValueCharFilter(
        lookup_expr='icontains'
    )
    port = django_filters.NumberFilter()
    port__gte = django_filters.NumberFilter(
        field_name='port',
        lookup_expr='gte',
    )
    port__lte = django_filters.NumberFilter(
        field_name='port',
        lookup_expr='lte',
    )
    is_public = django_filters.BooleanFilter()
    is_load_balanced = django_filters.BooleanFilter()
    authentication_required = django_filters.BooleanFilter()
    ssl_enabled = django_filters.BooleanFilter()

    class Meta:
        model = ApplicationEndpoint
        fields = ('id', 'name', 'description', 'comments')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(comments__icontains=value) |
            Q(url__icontains=value) |
            Q(protocol__icontains=value) |
            Q(path__icontains=value)
        )


class ApplicationPersonnelFilterSet(NetBoxModelFilterSet):
    application_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Application.objects.all(),
        label='Application (ID)',
    )
    application = django_filters.ModelMultipleChoiceFilter(
        field_name='application__slug',
        queryset=Application.objects.all(),
        to_field_name='slug',
        label='Application (slug)',
    )
    contact_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label='Contact (ID)',
    )
    contact = django_filters.ModelMultipleChoiceFilter(
        field_name='contact__name',
        queryset=Contact.objects.all(),
        to_field_name='name',
        label='Contact (name)',
    )
    role = django_filters.MultipleChoiceFilter(
        choices=PersonnelRoleChoices,
        null_value=None,
    )
    department = MultiValueCharFilter(
        lookup_expr='icontains'
    )
    title = MultiValueCharFilter(
        lookup_expr='icontains'
    )
    is_primary = django_filters.BooleanFilter()
    is_emergency_contact = django_filters.BooleanFilter()

    class Meta:
        model = ApplicationPersonnel
        fields = ('id', 'name', 'email', 'phone', 'notes')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(email__icontains=value) |
            Q(phone__icontains=value) |
            Q(department__icontains=value) |
            Q(title__icontains=value) |
            Q(notes__icontains=value)
        )