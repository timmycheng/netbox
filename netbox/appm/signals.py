import logging
from typing import Any

from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone

from .models import (
    ApplicationGroup, Application, ApplicationServer, 
    ApplicationEndpoint, ApplicationPersonnel
)
from .config import get_config

logger = logging.getLogger(__name__)


def clear_model_cache(model_name: str):
    """清除模型相关缓存"""
    if get_config('ENABLE_CACHING'):
        # 清除列表缓存
        cache_pattern = f'appm:{model_name}:*'
        # 由于Django缓存API限制，这里使用简单的缓存清理
        cache.clear()
        logger.debug(f'Cleared cache for model: {model_name}')


def validate_and_log_changes(instance, model_name: str):
    """验证数据并记录变更"""
    if instance.pk:
        try:
            old_instance = instance.__class__.objects.get(pk=instance.pk)
            changes = []

            # 检查常见字段的变更
            common_fields = ['name', 'status', 'description']
            for field in common_fields:
                if hasattr(instance, field) and hasattr(old_instance, field):
                    old_value = getattr(old_instance, field)
                    new_value = getattr(instance, field)
                    if old_value != new_value:
                        changes.append(f'{field}: {old_value} -> {new_value}')

            if changes:
                logger.info(f'{model_name} changes for {instance.name}: {changes}')

        except instance.__class__.DoesNotExist:
            pass


# ApplicationGroup 信号处理器
@receiver(pre_save, sender=ApplicationGroup)
def applicationgroup_pre_save(sender, instance, **kwargs):
    """应用组保存前处理"""
    validate_and_log_changes(instance, 'ApplicationGroup')


@receiver(post_save, sender=ApplicationGroup)
def applicationgroup_post_save(sender, instance, created, **kwargs):
    """应用组保存后处理"""
    clear_model_cache('applicationgroup')
    
    action = 'Created' if created else 'Updated'
    logger.info(f'{action} application group: {instance.name} (ID: {instance.pk})')


@receiver(post_delete, sender=ApplicationGroup)
def applicationgroup_post_delete(sender, instance, **kwargs):
    """应用组删除后处理"""
    clear_model_cache('applicationgroup')
    logger.warning(f'Deleted application group: {instance.name} (ID: {instance.pk})')


# Application 信号处理器
@receiver(pre_save, sender=Application)
def application_pre_save(sender, instance, **kwargs):
    """应用系统保存前处理"""
    validate_and_log_changes(instance, 'Application')
    
    # 验证版本号格式
    if instance.version:
        import re
        version_pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
        if not re.match(version_pattern, instance.version):
            logger.warning(f'Invalid version format for {instance.name}: {instance.version}')


@receiver(post_save, sender=Application)
def application_post_save(sender, instance, created, **kwargs):
    """应用系统保存后处理"""
    clear_model_cache('application')
    
    action = 'Created' if created else 'Updated'
    logger.info(f'{action} application: {instance.name} (ID: {instance.pk})')
    
    # 如果启用了通知功能
    if created and get_config('ENABLE_NOTIFICATIONS'):
        logger.info(f'Notification: New application {instance.name} created')


@receiver(post_delete, sender=Application)
def application_post_delete(sender, instance, **kwargs):
    """应用系统删除后处理"""
    clear_model_cache('application')
    logger.warning(f'Deleted application: {instance.name} (ID: {instance.pk})')


# ApplicationServer 信号处理器
@receiver(pre_save, sender=ApplicationServer)
def applicationserver_pre_save(sender, instance, **kwargs):
    """应用服务器保存前处理"""
    validate_and_log_changes(instance, 'ApplicationServer')
    
    # 验证服务器配置
    if instance.device and instance.virtual_machine:
        logger.error(
            f'ApplicationServer {instance.name} cannot have both device and VM'
        )
    
    # 验证资源配置
    if instance.cpu_cores and instance.cpu_cores <= 0:
        logger.warning(f'Invalid CPU cores for {instance.name}: {instance.cpu_cores}')
    
    if instance.memory_gb and instance.memory_gb <= 0:
        logger.warning(f'Invalid memory for {instance.name}: {instance.memory_gb}')


@receiver(post_save, sender=ApplicationServer)
def applicationserver_post_save(sender, instance, created, **kwargs):
    """应用服务器保存后处理"""
    clear_model_cache('applicationserver')
    
    action = 'Created' if created else 'Updated'
    logger.info(
        f'{action} application server: {instance.name} '
        f'for application {instance.application.name}'
    )


@receiver(post_delete, sender=ApplicationServer)
def applicationserver_post_delete(sender, instance, **kwargs):
    """应用服务器删除后处理"""
    clear_model_cache('applicationserver')
    logger.info(f'Deleted application server: {instance.name}')


# ApplicationEndpoint 信号处理器
@receiver(pre_save, sender=ApplicationEndpoint)
def applicationendpoint_pre_save(sender, instance, **kwargs):
    """应用端点保存前处理"""
    validate_and_log_changes(instance, 'ApplicationEndpoint')
    
    # 验证URL格式
    if instance.url:
        import re
        url_pattern = r'^https?://[\w\.-]+(?:\.[a-zA-Z]{2,})+(?:/[\w\.-]*)*/?(?:\?[\w&=%\.-]*)?$'
        if not re.match(url_pattern, instance.url):
            logger.warning(f'Invalid URL format for {instance.name}: {instance.url}')
    
    # 验证端口范围
    if instance.port and not (1 <= instance.port <= 65535):
        logger.warning(f'Invalid port for {instance.name}: {instance.port}')
    
    # 自动设置协议
    if instance.url and not instance.protocol:
        if instance.url.startswith('https://'):
            instance.protocol = 'HTTPS'
            instance.ssl_enabled = True
        elif instance.url.startswith('http://'):
            instance.protocol = 'HTTP'
            instance.ssl_enabled = False


@receiver(post_save, sender=ApplicationEndpoint)
def applicationendpoint_post_save(sender, instance, created, **kwargs):
    """应用端点保存后处理"""
    clear_model_cache('applicationendpoint')
    
    action = 'Created' if created else 'Updated'
    logger.info(
        f'{action} application endpoint: {instance.name} '
        f'for application {instance.application.name}'
    )
    
    # 如果是公开端点，记录特殊日志
    if instance.is_public and created:
        logger.info(f'Public endpoint created: {instance.name} - {instance.url}')


@receiver(post_delete, sender=ApplicationEndpoint)
def applicationendpoint_post_delete(sender, instance, **kwargs):
    """应用端点删除后处理"""
    clear_model_cache('applicationendpoint')
    logger.info(f'Deleted application endpoint: {instance.name}')


# ApplicationPersonnel 信号处理器
@receiver(pre_save, sender=ApplicationPersonnel)
def applicationpersonnel_pre_save(sender, instance, **kwargs):
    """应用人员保存前处理"""
    validate_and_log_changes(instance, 'ApplicationPersonnel')
    
    # 验证邮箱格式
    if instance.email:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, instance.email):
            logger.warning(f'Invalid email for {instance.name}: {instance.email}')
    
    # 验证电话格式
    if instance.phone:
        import re
        # 简单的电话号码验证
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', instance.phone)
        if not clean_phone.isdigit() or len(clean_phone) < 7:
            logger.warning(f'Invalid phone for {instance.name}: {instance.phone}')
    
    # 验证日期逻辑
    if instance.start_date and instance.end_date:
        if instance.start_date > instance.end_date:
            logger.error(
                f'Invalid date range for {instance.name}: '
                f'start_date ({instance.start_date}) > end_date ({instance.end_date})'
            )


@receiver(post_save, sender=ApplicationPersonnel)
def applicationpersonnel_post_save(sender, instance, created, **kwargs):
    """应用人员保存后处理"""
    clear_model_cache('applicationpersonnel')
    
    action = 'Created' if created else 'Updated'
    logger.info(
        f'{action} personnel: {instance.name} ({instance.role}) '
        f'for application {instance.application.name}'
    )
    
    # 如果是主要联系人，确保只有一个
    if instance.is_primary and created:
        # 将同一应用的其他主要联系人设置为非主要
        ApplicationPersonnel.objects.filter(
            application=instance.application,
            is_primary=True
        ).exclude(pk=instance.pk).update(is_primary=False)
        
        logger.info(f'Primary contact set for {instance.application.name}: {instance.name}')


@receiver(post_delete, sender=ApplicationPersonnel)
def applicationpersonnel_post_delete(sender, instance, **kwargs):
    """应用人员删除后处理"""
    clear_model_cache('applicationpersonnel')
    logger.info(f'Deleted personnel: {instance.name}')
    
    # 如果删除的是主要联系人，可能需要指定新的主要联系人
    if instance.is_primary:
        remaining_personnel = ApplicationPersonnel.objects.filter(
            application=instance.application
        ).first()
        
        if remaining_personnel:
            remaining_personnel.is_primary = True
            remaining_personnel.save()
            logger.info(
                f'New primary contact for {instance.application.name}: '
                f'{remaining_personnel.name}'
            )


# 通用信号处理器
@receiver([post_save, post_delete], sender=ApplicationServer)
@receiver([post_save, post_delete], sender=ApplicationEndpoint)
@receiver([post_save, post_delete], sender=ApplicationPersonnel)
def update_application_last_modified(sender, instance, **kwargs):
    """更新应用的最后修改时间"""
    if hasattr(instance, 'application') and instance.application:
        # 更新关联应用的最后修改时间
        Application.objects.filter(
            pk=instance.application.pk
        ).update(last_updated=timezone.now())
        
        logger.debug(
            f'Updated last_updated for application: {instance.application.name}'
        )