from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from . import filtersets, forms, models, tables


#
# Application Groups
#

@register_model_view(models.ApplicationGroup, 'list', detail=False)
class ApplicationGroupListView(generic.ObjectListView):
    queryset = models.ApplicationGroup.objects.all()
    table = tables.ApplicationGroupTable
    filterset = filtersets.ApplicationGroupFilterSet


@register_model_view(models.ApplicationGroup)
class ApplicationGroupView(generic.ObjectView):
    queryset = models.ApplicationGroup.objects.all()


@register_model_view(models.ApplicationGroup, 'edit')
@register_model_view(models.ApplicationGroup, 'add', detail=False)
class ApplicationGroupEditView(generic.ObjectEditView):
    queryset = models.ApplicationGroup.objects.all()
    form = forms.ApplicationGroupForm


@register_model_view(models.ApplicationGroup, 'delete')
class ApplicationGroupDeleteView(generic.ObjectDeleteView):
    queryset = models.ApplicationGroup.objects.all()


@register_model_view(models.ApplicationGroup, 'bulk_import', detail=False)
class ApplicationGroupBulkImportView(generic.BulkImportView):
    queryset = models.ApplicationGroup.objects.all()
    model_form = forms.ApplicationGroupImportForm


@register_model_view(models.ApplicationGroup, 'bulk_edit', detail=False)
class ApplicationGroupBulkEditView(generic.BulkEditView):
    queryset = models.ApplicationGroup.objects.all()
    filterset = filtersets.ApplicationGroupFilterSet
    table = tables.ApplicationGroupTable
    form = forms.ApplicationGroupBulkEditForm


@register_model_view(models.ApplicationGroup, 'bulk_delete', detail=False)
class ApplicationGroupBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ApplicationGroup.objects.all()
    filterset = filtersets.ApplicationGroupFilterSet
    table = tables.ApplicationGroupTable


#
# Applications
#

@register_model_view(models.Application, 'list', detail=False)
class ApplicationListView(generic.ObjectListView):
    queryset = models.Application.objects.prefetch_related('group', 'tenant')
    table = tables.ApplicationTable
    filterset = filtersets.ApplicationFilterSet


@register_model_view(models.Application)
class ApplicationView(generic.ObjectView):
    queryset = models.Application.objects.prefetch_related('group', 'tenant')


@register_model_view(models.Application, 'edit')
@register_model_view(models.Application, 'add', detail=False)
class ApplicationEditView(generic.ObjectEditView):
    queryset = models.Application.objects.all()
    form = forms.ApplicationForm


@register_model_view(models.Application, 'delete')
class ApplicationDeleteView(generic.ObjectDeleteView):
    queryset = models.Application.objects.all()


@register_model_view(models.Application, 'bulk_import', detail=False)
class ApplicationBulkImportView(generic.BulkImportView):
    queryset = models.Application.objects.all()
    model_form = forms.ApplicationImportForm


@register_model_view(models.Application, 'bulk_edit', detail=False)
class ApplicationBulkEditView(generic.BulkEditView):
    queryset = models.Application.objects.all()
    filterset = filtersets.ApplicationFilterSet
    table = tables.ApplicationTable
    form = forms.ApplicationBulkEditForm


@register_model_view(models.Application, 'bulk_delete', detail=False)
class ApplicationBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Application.objects.all()
    filterset = filtersets.ApplicationFilterSet
    table = tables.ApplicationTable


#
# Application Servers
#

@register_model_view(models.ApplicationServer, 'list', detail=False)
class ApplicationServerListView(generic.ObjectListView):
    queryset = models.ApplicationServer.objects.prefetch_related(
        'application', 'device', 'virtual_machine', 'primary_ip4', 'primary_ip6'
    )
    table = tables.ApplicationServerTable
    filterset = filtersets.ApplicationServerFilterSet


@register_model_view(models.ApplicationServer)
class ApplicationServerView(generic.ObjectView):
    queryset = models.ApplicationServer.objects.prefetch_related(
        'application', 'device', 'virtual_machine', 'primary_ip4', 'primary_ip6'
    )


@register_model_view(models.ApplicationServer, 'edit')
@register_model_view(models.ApplicationServer, 'add', detail=False)
class ApplicationServerEditView(generic.ObjectEditView):
    queryset = models.ApplicationServer.objects.all()
    form = forms.ApplicationServerForm


@register_model_view(models.ApplicationServer, 'delete')
class ApplicationServerDeleteView(generic.ObjectDeleteView):
    queryset = models.ApplicationServer.objects.all()


@register_model_view(models.ApplicationServer, 'bulk_import', detail=False)
class ApplicationServerBulkImportView(generic.BulkImportView):
    queryset = models.ApplicationServer.objects.all()
    model_form = forms.ApplicationServerImportForm


@register_model_view(models.ApplicationServer, 'bulk_edit', detail=False)
class ApplicationServerBulkEditView(generic.BulkEditView):
    queryset = models.ApplicationServer.objects.all()
    filterset = filtersets.ApplicationServerFilterSet
    table = tables.ApplicationServerTable
    form = forms.ApplicationServerBulkEditForm


@register_model_view(models.ApplicationServer, 'bulk_delete', detail=False)
class ApplicationServerBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ApplicationServer.objects.all()
    filterset = filtersets.ApplicationServerFilterSet
    table = tables.ApplicationServerTable


#
# Application Endpoints
#

@register_model_view(models.ApplicationEndpoint, 'list', detail=False)
class ApplicationEndpointListView(generic.ObjectListView):
    queryset = models.ApplicationEndpoint.objects.prefetch_related(
        'application', 'server', 'ip_address'
    )
    table = tables.ApplicationEndpointTable
    filterset = filtersets.ApplicationEndpointFilterSet


@register_model_view(models.ApplicationEndpoint)
class ApplicationEndpointView(generic.ObjectView):
    queryset = models.ApplicationEndpoint.objects.prefetch_related(
        'application', 'server', 'ip_address'
    )


@register_model_view(models.ApplicationEndpoint, 'edit')
@register_model_view(models.ApplicationEndpoint, 'add', detail=False)
class ApplicationEndpointEditView(generic.ObjectEditView):
    queryset = models.ApplicationEndpoint.objects.all()
    form = forms.ApplicationEndpointForm


@register_model_view(models.ApplicationEndpoint, 'delete')
class ApplicationEndpointDeleteView(generic.ObjectDeleteView):
    queryset = models.ApplicationEndpoint.objects.all()


@register_model_view(models.ApplicationEndpoint, 'bulk_import', detail=False)
class ApplicationEndpointBulkImportView(generic.BulkImportView):
    queryset = models.ApplicationEndpoint.objects.all()
    model_form = forms.ApplicationEndpointImportForm


@register_model_view(models.ApplicationEndpoint, 'bulk_edit', detail=False)
class ApplicationEndpointBulkEditView(generic.BulkEditView):
    queryset = models.ApplicationEndpoint.objects.all()
    filterset = filtersets.ApplicationEndpointFilterSet
    table = tables.ApplicationEndpointTable
    form = forms.ApplicationEndpointBulkEditForm


@register_model_view(models.ApplicationEndpoint, 'bulk_delete', detail=False)
class ApplicationEndpointBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ApplicationEndpoint.objects.all()
    filterset = filtersets.ApplicationEndpointFilterSet
    table = tables.ApplicationEndpointTable


#
# Application Personnel
#

@register_model_view(models.ApplicationPersonnel, 'list', detail=False)
class ApplicationPersonnelListView(generic.ObjectListView):
    queryset = models.ApplicationPersonnel.objects.prefetch_related(
        'application', 'contact'
    )
    table = tables.ApplicationPersonnelTable
    filterset = filtersets.ApplicationPersonnelFilterSet


@register_model_view(models.ApplicationPersonnel)
class ApplicationPersonnelView(generic.ObjectView):
    queryset = models.ApplicationPersonnel.objects.prefetch_related(
        'application', 'contact'
    )


@register_model_view(models.ApplicationPersonnel, 'edit')
@register_model_view(models.ApplicationPersonnel, 'add', detail=False)
class ApplicationPersonnelEditView(generic.ObjectEditView):
    queryset = models.ApplicationPersonnel.objects.all()
    form = forms.ApplicationPersonnelForm


@register_model_view(models.ApplicationPersonnel, 'delete')
class ApplicationPersonnelDeleteView(generic.ObjectDeleteView):
    queryset = models.ApplicationPersonnel.objects.all()


@register_model_view(models.ApplicationPersonnel, 'bulk_import', detail=False)
class ApplicationPersonnelBulkImportView(generic.BulkImportView):
    queryset = models.ApplicationPersonnel.objects.all()
    model_form = forms.ApplicationPersonnelImportForm


@register_model_view(models.ApplicationPersonnel, 'bulk_edit', detail=False)
class ApplicationPersonnelBulkEditView(generic.BulkEditView):
    queryset = models.ApplicationPersonnel.objects.all()
    filterset = filtersets.ApplicationPersonnelFilterSet
    table = tables.ApplicationPersonnelTable
    form = forms.ApplicationPersonnelBulkEditForm


@register_model_view(models.ApplicationPersonnel, 'bulk_delete', detail=False)
class ApplicationPersonnelBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ApplicationPersonnel.objects.all()
    filterset = filtersets.ApplicationPersonnelFilterSet
    table = tables.ApplicationPersonnelTable