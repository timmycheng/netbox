from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from netbox.models import PrimaryModel
from tenancy.models import Contact
from appm.choices import *

__all__ = (
    'ApplicationPersonnel',
)


class ApplicationPersonnel(PrimaryModel):
    """
    应用系统人员模型，用于管理应用系统相关的人员信息
    """
    application = models.ForeignKey(
        to='appm.Application',
        on_delete=models.CASCADE,
        related_name='personnel',
        verbose_name=_('application')
    )
    contact = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.SET_NULL,
        related_name='application_personnel',
        blank=True,
        null=True,
        verbose_name=_('contact'),
        help_text=_('关联的联系人')
    )
    name = models.CharField(
        verbose_name=_('name'),
        max_length=100,
        help_text=_('人员姓名'),
        db_collation="natural_sort"
    )
    role = models.CharField(
        verbose_name=_('role'),
        max_length=50,
        choices=PersonnelRoleChoices,
        help_text=_('在应用系统中的角色')
    )
    email = models.EmailField(
        verbose_name=_('email'),
        blank=True,
        help_text=_('电子邮箱')
    )
    phone = models.CharField(
        verbose_name=_('phone'),
        max_length=50,
        blank=True,
        help_text=_('联系电话')
    )
    department = models.CharField(
        verbose_name=_('department'),
        max_length=100,
        blank=True,
        help_text=_('所属部门')
    )
    title = models.CharField(
        verbose_name=_('title'),
        max_length=100,
        blank=True,
        help_text=_('职位')
    )
    is_primary = models.BooleanField(
        verbose_name=_('is primary'),
        default=False,
        help_text=_('是否为主要负责人')
    )
    is_emergency_contact = models.BooleanField(
        verbose_name=_('is emergency contact'),
        default=False,
        help_text=_('是否为紧急联系人')
    )
    start_date = models.DateField(
        verbose_name=_('start date'),
        blank=True,
        null=True,
        help_text=_('开始负责日期')
    )
    end_date = models.DateField(
        verbose_name=_('end date'),
        blank=True,
        null=True,
        help_text=_('结束负责日期')
    )
    notes = models.TextField(
        verbose_name=_('notes'),
        blank=True,
        help_text=_('备注信息')
    )

    clone_fields = (
        'application', 'role', 'department', 'title', 'is_primary', 'is_emergency_contact', 'description',
    )

    class Meta:
        ordering = ('application', 'role', 'name')
        verbose_name = _('application personnel')
        verbose_name_plural = _('application personnel')
        constraints = [
            models.UniqueConstraint(
                fields=['application', 'name', 'role'],
                name='%(app_label)s_%(class)s_unique_application_name_role'
            )
        ]

    def __str__(self):
        return f'{self.application.name} - {self.name} ({self.get_role_display()})'

    def clean(self):
        super().clean()
        
        # 确保结束日期不早于开始日期
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({
                'end_date': _('结束日期不能早于开始日期')
            })
        
        # 如果关联了联系人，可以从联系人自动填充一些信息
        if self.contact and not self.email and hasattr(self.contact, 'email'):
            self.email = self.contact.email
        
        if self.contact and not self.phone and hasattr(self.contact, 'phone'):
            self.phone = self.contact.phone

    @property
    def is_active(self):
        """判断人员是否仍在负责该应用系统"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.start_date and self.start_date > today:
            return False
        
        if self.end_date and self.end_date < today:
            return False
        
        return True

    @property
    def contact_info(self):
        """返回联系方式摘要"""
        info = []
        if self.email:
            info.append(f'Email: {self.email}')
        if self.phone:
            info.append(f'Phone: {self.phone}')
        return ' | '.join(info) if info else None