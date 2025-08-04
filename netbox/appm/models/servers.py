from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel
from appm.choices import *

__all__ = (
    'ApplicationServer',
)


class ApplicationServer(PrimaryModel):
    """
    应用系统服务器模型，用于管理应用系统下的服务器资源
    """
    application = models.ForeignKey(
        to='appm.Application',
        on_delete=models.CASCADE,
        related_name='servers',
        verbose_name=_('application')
    )
    device = models.ForeignKey(
        to='dcim.Device',
        on_delete=models.CASCADE,
        related_name='application_servers',
        blank=True,
        null=True,
        verbose_name=_('device'),
        help_text=_('关联的物理设备')
    )
    virtual_machine = models.ForeignKey(
        to='virtualization.VirtualMachine',
        on_delete=models.CASCADE,
        related_name='application_servers',
        blank=True,
        null=True,
        verbose_name=_('virtual machine'),
        help_text=_('关联的虚拟机')
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        help_text=_('服务器在应用系统中的名称或标识'),
        db_collation="natural_sort"
    )
    role = models.CharField(
        verbose_name=_('role'),
        max_length=50,
        choices=ServerRoleChoices,
        help_text=_('服务器在应用系统中的角色')
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=ServerStatusChoices,
        default=ServerStatusChoices.STATUS_ACTIVE
    )
    primary_ip4 = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        related_name='primary_application_servers_v4',
        blank=True,
        null=True,
        verbose_name=_('primary IPv4'),
        help_text=_('主要IPv4地址')
    )
    primary_ip6 = models.ForeignKey(
        to='ipam.IPAddress',
        on_delete=models.SET_NULL,
        related_name='primary_application_servers_v6',
        blank=True,
        null=True,
        verbose_name=_('primary IPv6'),
        help_text=_('主要IPv6地址')
    )
    additional_ips = models.ManyToManyField(
        to='ipam.IPAddress',
        related_name='additional_application_servers',
        blank=True,
        verbose_name=_('additional IP addresses'),
        help_text=_('额外的IP地址')
    )
    cpu_cores = models.PositiveSmallIntegerField(
        verbose_name=_('CPU cores'),
        blank=True,
        null=True,
        help_text=_('CPU核心数')
    )
    memory_gb = models.PositiveIntegerField(
        verbose_name=_('memory (GB)'),
        blank=True,
        null=True,
        help_text=_('内存大小(GB)')
    )
    storage_gb = models.PositiveIntegerField(
        verbose_name=_('storage (GB)'),
        blank=True,
        null=True,
        help_text=_('存储大小(GB)')
    )
    operating_system = models.CharField(
        verbose_name=_('operating system'),
        max_length=100,
        blank=True,
        help_text=_('操作系统')
    )
    middleware = models.TextField(
        verbose_name=_('middleware'),
        blank=True,
        help_text=_('中间件信息')
    )

    clone_fields = (
        'application', 'role', 'status', 'cpu_cores', 'memory_gb', 'storage_gb', 'operating_system', 'description',
    )

    class Meta:
        ordering = ('application', 'name')
        verbose_name = _('application server')
        verbose_name_plural = _('application servers')
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
        
        # 确保设备和虚拟机不能同时为空
        if not self.device and not self.virtual_machine:
            raise ValidationError({
                '__all__': _('必须关联一个设备或虚拟机')
            })
        
        # 确保设备和虚拟机不能同时设置
        if self.device and self.virtual_machine:
            raise ValidationError({
                '__all__': _('不能同时关联设备和虚拟机')
            })

    def get_status_color(self):
        return ServerStatusChoices.colors.get(self.status)

    @property
    def primary_ip(self):
        """返回主要IP地址（优先IPv4）"""
        return self.primary_ip4 or self.primary_ip6

    @property
    def host(self):
        """返回关联的主机（设备或虚拟机）"""
        return self.device or self.virtual_machine