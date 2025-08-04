from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel, NestedGroupModel
from netbox.models.features import ContactsMixin, ImageAttachmentsMixin
from appm.choices import *

__all__ = (
    'Application',
    'ApplicationGroup',
)


class ApplicationGroup(NestedGroupModel):
    """
    应用系统分组，用于对应用系统进行分类管理
    """
    class Meta:
        ordering = ('name',)
        constraints = (
            models.UniqueConstraint(
                fields=('parent', 'name'),
                name='%(app_label)s_%(class)s_unique_parent_name'
            ),
        )
        verbose_name = _('application group')
        verbose_name_plural = _('application groups')


class Application(ContactsMixin, ImageAttachmentsMixin, PrimaryModel):
    """
    应用系统模型，用于管理应用系统的基本信息
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        help_text=_('应用系统名称'),
        db_collation="natural_sort"
    )
    slug = models.SlugField(
        verbose_name=_('slug'),
        max_length=100,
        unique=True
    )
    group = models.ForeignKey(
        to='appm.ApplicationGroup',
        on_delete=models.SET_NULL,
        related_name='applications',
        blank=True,
        null=True,
        verbose_name=_('group')
    )
    status = models.CharField(
        verbose_name=_('status'),
        max_length=50,
        choices=ApplicationStatusChoices,
        default=ApplicationStatusChoices.STATUS_ACTIVE
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='applications',
        blank=True,
        null=True,
        verbose_name=_('tenant')
    )
    version = models.CharField(
        verbose_name=_('version'),
        max_length=50,
        blank=True,
        help_text=_('应用系统版本')
    )
    owner = models.CharField(
        verbose_name=_('owner'),
        max_length=100,
        blank=True,
        help_text=_('应用系统负责人')
    )
    business_unit = models.CharField(
        verbose_name=_('business unit'),
        max_length=100,
        blank=True,
        help_text=_('所属业务单元')
    )
    criticality = models.CharField(
        verbose_name=_('criticality'),
        max_length=50,
        choices=ApplicationCriticalityChoices,
        default=ApplicationCriticalityChoices.MEDIUM,
        help_text=_('应用系统重要性等级')
    )
    environment = models.CharField(
        verbose_name=_('environment'),
        max_length=50,
        choices=ApplicationEnvironmentChoices,
        default=ApplicationEnvironmentChoices.PRODUCTION,
        help_text=_('应用系统环境')
    )

    clone_fields = (
        'group', 'status', 'tenant', 'owner', 'business_unit', 'criticality', 'environment', 'description',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = _('application')
        verbose_name_plural = _('applications')
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'environment'],
                name='%(app_label)s_%(class)s_unique_name_environment'
            )
        ]

    def __str__(self):
        return self.name

    def get_status_color(self):
        return ApplicationStatusChoices.colors.get(self.status)