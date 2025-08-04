from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel
from appm.choices import *

__all__ = (
    'ApplicationEndpoint',
)


class ApplicationEndpoint(PrimaryModel):
    """
    应用系统端点模型，用于管理应用系统的URL端点、端口映射等
    """
    application = models.ForeignKey(
        to='appm.Application',
        on_delete=models.CASCADE,
        related_name='endpoints',
        verbose_name=_('application')
    )
    server = models.ForeignKey(
        to='appm.ApplicationServer',
        on_delete=models.CASCADE,
        related_name='endpoints',
        blank=True,
        null=True,
        verbose_name=_('server'),
        help_text=_('关联的应用服务器')
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        help_text=_('端点名称或标识'),
        db_collation="natural_sort"
    )
    type = models.CharField(
        verbose_name=_('type'),
        max_length=50,
        choices=EndpointTypeChoices,
        help_text=_('端点类型')
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=EndpointStatusChoices,
        default=EndpointStatusChoices.STATUS_ACTIVE
    )
    url = models.URLField(
        verbose_name=_('URL'),
        max_length=500,
        blank=True,
        help_text=_('完整的URL地址')
    )
    ip_address = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        related_name='application_endpoints',
        blank=True,
        null=True,
        verbose_name=_('IP address'),
        help_text=_('IP地址')
    )
    port = models.PositiveIntegerField(
        verbose_name=_('port'),
        blank=True,
        null=True,
        help_text=_('端口号')
    )
    protocol = models.CharField(
        verbose_name=_('protocol'),
        max_length=20,
        blank=True,
        help_text=_('协议（如HTTP、HTTPS、TCP、UDP等）')
    )
    path = models.CharField(
        verbose_name=_('path'),
        max_length=500,
        blank=True,
        help_text=_('URL路径')
    )
    is_public = models.BooleanField(
        verbose_name=_('is public'),
        default=False,
        help_text=_('是否为公网访问端点')
    )
    is_load_balanced = models.BooleanField(
        verbose_name=_('is load balanced'),
        default=False,
        help_text=_('是否经过负载均衡')
    )
    health_check_url = models.URLField(
        verbose_name=_('health check URL'),
        max_length=500,
        blank=True,
        help_text=_('健康检查URL')
    )
    authentication_required = models.BooleanField(
        verbose_name=_('authentication required'),
        default=False,
        help_text=_('是否需要身份验证')
    )
    ssl_enabled = models.BooleanField(
        verbose_name=_('SSL enabled'),
        default=False,
        help_text=_('是否启用SSL/TLS')
    )
    documentation_url = models.URLField(
        verbose_name=_('documentation URL'),
        max_length=500,
        blank=True,
        help_text=_('文档URL')
    )

    clone_fields = (
        'application', 'server', 'type', 'status', 'protocol', 'is_public', 'is_load_balanced',
        'authentication_required', 'ssl_enabled', 'description',
    )

    class Meta:
        ordering = ('application', 'name')
        verbose_name = _('application endpoint')
        verbose_name_plural = _('application endpoints')
        constraints = [
            models.UniqueConstraint(
                fields=['application', 'name'],
                name='%(app_label)s_%(class)s_unique_application_name'
            )
        ]

    def __str__(self):
        return f'{self.application.name} - {self.name}'

    def clean(self):
        super().clean()
        
        # 如果设置了服务器，确保服务器属于同一个应用系统
        if self.server and self.server.application != self.application:
            raise ValidationError({
                'server': _('服务器必须属于同一个应用系统')
            })
        
        # 如果设置了端口，确保端口号在有效范围内
        if self.port is not None and (self.port < 1 or self.port > 65535):
            raise ValidationError({
                'port': _('端口号必须在1-65535范围内')
            })
        
        # 如果类型是Web UI或API，建议设置URL
        if self.type in [EndpointTypeChoices.WEB_UI, EndpointTypeChoices.API] and not self.url:
            # 这里只是警告，不阻止保存
            pass

    def get_status_color(self):
        return EndpointStatusChoices.colors.get(self.status)

    @property
    def full_address(self):
        """返回完整的地址信息"""
        if self.url:
            return self.url
        
        parts = []
        if self.protocol:
            parts.append(f'{self.protocol.lower()}://')
        
        if self.ip_address:
            parts.append(str(self.ip_address.address.ip))
        
        if self.port:
            parts.append(f':{self.port}')
        
        if self.path:
            if not self.path.startswith('/'):
                parts.append('/')
            parts.append(self.path)
        
        return ''.join(parts) if parts else None