import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Application, ApplicationServer, ApplicationEndpoint, ApplicationPersonnel

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Application)
def application_post_save(sender, instance, created, **kwargs):
    """
    应用系统保存后的信号处理
    """
    if created:
        logger.info(f'Created new application: {instance.name}')
    else:
        logger.info(f'Updated application: {instance.name}')


@receiver(post_delete, sender=Application)
def application_post_delete(sender, instance, **kwargs):
    """
    应用系统删除后的信号处理
    """
    logger.info(f'Deleted application: {instance.name}')


@receiver(post_save, sender=ApplicationServer)
def application_server_post_save(sender, instance, created, **kwargs):
    """
    应用服务器保存后的信号处理
    """
    if created:
        logger.info(f'Created new application server: {instance.name} for {instance.application.name}')
    else:
        logger.info(f'Updated application server: {instance.name} for {instance.application.name}')


@receiver(post_save, sender=ApplicationEndpoint)
def application_endpoint_post_save(sender, instance, created, **kwargs):
    """
    应用端点保存后的信号处理
    """
    if created:
        logger.info(f'Created new application endpoint: {instance.name} for {instance.application.name}')
    else:
        logger.info(f'Updated application endpoint: {instance.name} for {instance.application.name}')


@receiver(post_save, sender=ApplicationPersonnel)
def application_personnel_post_save(sender, instance, created, **kwargs):
    """
    应用人员保存后的信号处理
    """
    if created:
        logger.info(f'Added personnel: {instance.name} to application {instance.application.name}')
    else:
        logger.info(f'Updated personnel: {instance.name} for application {instance.application.name}')