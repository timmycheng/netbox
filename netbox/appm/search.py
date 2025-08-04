from netbox.search import SearchIndex, register_search
from . import models


@register_search
class ApplicationIndex(SearchIndex):
    model = models.Application
    fields = (
        ('name', 100),
        ('slug', 110),
        ('description', 500),
        ('comments', 5000),
        ('owner', 300),
        ('business_unit', 300),
        ('version', 200),
    )
    display_attrs = ('group', 'status', 'tenant', 'environment', 'criticality')


@register_search
class ApplicationGroupIndex(SearchIndex):
    model = models.ApplicationGroup
    fields = (
        ('name', 100),
        ('slug', 110),
        ('description', 500),
        ('comments', 5000),
    )


@register_search
class ApplicationServerIndex(SearchIndex):
    model = models.ApplicationServer
    fields = (
        ('name', 100),
        ('description', 500),
        ('comments', 5000),
        ('operating_system', 300),
        ('middleware', 300),
    )
    display_attrs = ('application', 'role', 'status', 'host')


@register_search
class ApplicationEndpointIndex(SearchIndex):
    model = models.ApplicationEndpoint
    fields = (
        ('name', 100),
        ('url', 200),
        ('path', 300),
        ('description', 500),
        ('comments', 5000),
        ('protocol', 200),
    )
    display_attrs = ('application', 'type', 'status', 'server')


@register_search
class ApplicationPersonnelIndex(SearchIndex):
    model = models.ApplicationPersonnel
    fields = (
        ('name', 100),
        ('email', 200),
        ('phone', 200),
        ('department', 300),
        ('title', 300),
        ('description', 500),
        ('comments', 5000),
        ('notes', 300),
    )
    display_attrs = ('application', 'role', 'department', 'is_primary')