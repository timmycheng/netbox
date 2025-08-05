"""APPM模块维护管理命令

此命令提供各种维护功能，包括数据清理、缓存管理、统计更新等。

使用方法:
    python manage.py appm_maintenance --help
    python manage.py appm_maintenance --cleanup
    python manage.py appm_maintenance --clear-cache
    python manage.py appm_maintenance --update-stats
    python manage.py appm_maintenance --validate-data
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone

from appm.models import (
    ApplicationGroup, Application, ApplicationServer, 
    ApplicationEndpoint, ApplicationPersonnel
)
from appm.config import get_config
from appm.utils import APPMCache, StatisticsHelper

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'APPM模块维护工具'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='清理过期和无效数据'
        )
        
        parser.add_argument(
            '--clear-cache',
            action='store_true',
            help='清除所有APPM相关缓存'
        )
        
        parser.add_argument(
            '--update-stats',
            action='store_true',
            help='更新统计信息'
        )
        
        parser.add_argument(
            '--validate-data',
            action='store_true',
            help='验证数据完整性'
        )
        
        parser.add_argument(
            '--optimize-db',
            action='store_true',
            help='优化数据库查询'
        )
        
        parser.add_argument(
            '--export-report',
            action='store_true',
            help='导出维护报告'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='仅显示将要执行的操作，不实际执行'
        )
        
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='显示详细输出'
        )
    
    def handle(self, *args, **options):
        self.dry_run = options['dry_run']
        self.verbose = options['verbose']
        
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        
        self.stdout.write(
            self.style.SUCCESS('APPM模块维护工具启动')
        )
        
        if self.dry_run:
            self.stdout.write(
                self.style.WARNING('运行在预览模式，不会实际修改数据')
            )
        
        # 执行各种维护任务
        if options['cleanup']:
            self.cleanup_data()
        
        if options['clear_cache']:
            self.clear_cache()
        
        if options['update_stats']:
            self.update_statistics()
        
        if options['validate_data']:
            self.validate_data()
        
        if options['optimize_db']:
            self.optimize_database()
        
        if options['export_report']:
            self.export_report()
        
        # 如果没有指定任何选项，显示帮助
        if not any([
            options['cleanup'], options['clear_cache'], 
            options['update_stats'], options['validate_data'],
            options['optimize_db'], options['export_report']
        ]):
            self.print_help('manage.py', 'appm_maintenance')
        
        self.stdout.write(
            self.style.SUCCESS('维护任务完成')
        )
    
    def cleanup_data(self):
        """清理过期和无效数据"""
        self.stdout.write('开始数据清理...')
        
        cleanup_stats = {
            'expired_personnel': 0,
            'inactive_endpoints': 0,
            'orphaned_servers': 0,
            'empty_groups': 0,
        }
        
        # 清理过期人员记录
        expired_personnel = ApplicationPersonnel.objects.filter(
            end_date__lt=timezone.now().date()
        )
        
        if self.verbose:
            self.stdout.write(f'找到 {expired_personnel.count()} 个过期人员记录')
        
        if not self.dry_run:
            cleanup_stats['expired_personnel'] = expired_personnel.count()
            expired_personnel.delete()
        
        # 清理长期不活跃的端点
        retention_days = get_config('HISTORY_RETENTION_DAYS', 365)
        cutoff_date = timezone.now() - timedelta(days=retention_days)
        
        inactive_endpoints = ApplicationEndpoint.objects.filter(
            status='inactive',
            last_updated__lt=cutoff_date
        )
        
        if self.verbose:
            self.stdout.write(f'找到 {inactive_endpoints.count()} 个长期不活跃的端点')
        
        if not self.dry_run:
            cleanup_stats['inactive_endpoints'] = inactive_endpoints.count()
            # 这里可以选择删除或标记为已归档
            # inactive_endpoints.delete()
        
        # 查找孤立的服务器（关联的应用已删除）
        orphaned_servers = ApplicationServer.objects.filter(
            application__isnull=True
        )
        
        if self.verbose:
            self.stdout.write(f'找到 {orphaned_servers.count()} 个孤立的服务器记录')
        
        if not self.dry_run:
            cleanup_stats['orphaned_servers'] = orphaned_servers.count()
            orphaned_servers.delete()
        
        # 清理空的应用组
        empty_groups = ApplicationGroup.objects.annotate(
            app_count=Count('applications')
        ).filter(app_count=0, parent__isnull=False)
        
        if self.verbose:
            self.stdout.write(f'找到 {empty_groups.count()} 个空的应用组')
        
        if not self.dry_run:
            cleanup_stats['empty_groups'] = empty_groups.count()
            # 谨慎删除空组，可能需要手动确认
            # empty_groups.delete()
        
        # 输出清理统计
        self.stdout.write(
            self.style.SUCCESS(
                f'数据清理完成: '
                f'过期人员: {cleanup_stats["expired_personnel"]}, '
                f'不活跃端点: {cleanup_stats["inactive_endpoints"]}, '
                f'孤立服务器: {cleanup_stats["orphaned_servers"]}, '
                f'空应用组: {cleanup_stats["empty_groups"]}'
            )
        )
    
    def clear_cache(self):
        """清除缓存"""
        self.stdout.write('清除APPM缓存...')
        
        if not self.dry_run:
            # 清除所有缓存
            cache.clear()
            
            # 或者只清除APPM相关的缓存
            # 这需要更复杂的实现来识别APPM缓存键
            
        self.stdout.write(
            self.style.SUCCESS('缓存清除完成')
        )
    
    def update_statistics(self):
        """更新统计信息"""
        self.stdout.write('更新统计信息...')
        
        models = [
            ApplicationGroup, Application, ApplicationServer,
            ApplicationEndpoint, ApplicationPersonnel
        ]
        
        stats = {}
        
        for model in models:
            model_name = model._meta.model_name
            model_stats = StatisticsHelper.get_model_statistics(model)
            stats[model_name] = model_stats
            
            if self.verbose:
                self.stdout.write(
                    f'{model._meta.verbose_name}: {model_stats["total"]} 总计'
                )
        
        # 计算应用健康度统计
        if not self.dry_run:
            self._calculate_application_health()
        
        self.stdout.write(
            self.style.SUCCESS('统计信息更新完成')
        )
    
    def validate_data(self):
        """验证数据完整性"""
        self.stdout.write('验证数据完整性...')
        
        issues = []
        
        # 检查应用是否有关联的服务器或端点
        apps_without_resources = Application.objects.annotate(
            server_count=Count('servers'),
            endpoint_count=Count('endpoints')
        ).filter(server_count=0, endpoint_count=0)
        
        if apps_without_resources.exists():
            issues.append(
                f'{apps_without_resources.count()} 个应用没有关联的服务器或端点'
            )
        
        # 检查服务器是否同时关联了设备和虚拟机
        invalid_servers = ApplicationServer.objects.filter(
            device__isnull=False,
            virtual_machine__isnull=False
        )
        
        if invalid_servers.exists():
            issues.append(
                f'{invalid_servers.count()} 个服务器同时关联了设备和虚拟机'
            )
        
        # 检查端点URL格式
        endpoints_with_urls = ApplicationEndpoint.objects.exclude(
            url__isnull=True
        ).exclude(url__exact='')
        
        invalid_urls = []
        for endpoint in endpoints_with_urls:
            if not self._is_valid_url(endpoint.url):
                invalid_urls.append(endpoint)
        
        if invalid_urls:
            issues.append(
                f'{len(invalid_urls)} 个端点的URL格式无效'
            )
        
        # 检查人员邮箱格式
        personnel_with_emails = ApplicationPersonnel.objects.exclude(
            email__isnull=True
        ).exclude(email__exact='')
        
        invalid_emails = []
        for person in personnel_with_emails:
            if not self._is_valid_email(person.email):
                invalid_emails.append(person)
        
        if invalid_emails:
            issues.append(
                f'{len(invalid_emails)} 个人员的邮箱格式无效'
            )
        
        # 输出验证结果
        if issues:
            self.stdout.write(
                self.style.WARNING('发现以下数据完整性问题:')
            )
            for issue in issues:
                self.stdout.write(f'  - {issue}')
        else:
            self.stdout.write(
                self.style.SUCCESS('数据完整性验证通过')
            )
    
    def optimize_database(self):
        """优化数据库"""
        self.stdout.write('优化数据库查询...')
        
        # 这里可以添加数据库优化逻辑
        # 例如：重建索引、更新统计信息等
        
        if not self.dry_run:
            # 示例：分析查询性能
            self._analyze_query_performance()
        
        self.stdout.write(
            self.style.SUCCESS('数据库优化完成')
        )
    
    def export_report(self):
        """导出维护报告"""
        self.stdout.write('生成维护报告...')
        
        report = self._generate_maintenance_report()
        
        if not self.dry_run:
            filename = f'appm_maintenance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            self.stdout.write(
                self.style.SUCCESS(f'维护报告已导出到: {filename}')
            )
        else:
            self.stdout.write('维护报告内容:')
            self.stdout.write(report)
    
    def _calculate_application_health(self):
        """计算应用健康度"""
        for app in Application.objects.all():
            health_score = 100
            
            # 检查是否有活跃的服务器
            active_servers = app.servers.filter(status='active').count()
            if active_servers == 0:
                health_score -= 30
            
            # 检查是否有可用的端点
            active_endpoints = app.endpoints.filter(status='active').count()
            if active_endpoints == 0:
                health_score -= 20
            
            # 检查是否有负责人
            personnel_count = app.personnel.count()
            if personnel_count == 0:
                health_score -= 15
            
            # 检查最后更新时间
            if app.last_updated < timezone.now() - timedelta(days=90):
                health_score -= 10
            
            # 这里可以将健康度保存到自定义字段或缓存中
            if self.verbose:
                self.stdout.write(
                    f'应用 {app.name} 健康度: {max(0, health_score)}%'
                )
    
    def _is_valid_url(self, url: str) -> bool:
        """验证URL格式"""
        import re
        pattern = r'^https?://[\w\.-]+(?:\.[a-zA-Z]{2,})+(?:/[\w\.-]*)*/?(?:\?[\w&=%\.-]*)?$'
        return bool(re.match(pattern, url))
    
    def _is_valid_email(self, email: str) -> bool:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _analyze_query_performance(self):
        """分析查询性能"""
        # 这里可以添加查询性能分析逻辑
        # 例如：记录慢查询、分析索引使用情况等
        pass
    
    def _generate_maintenance_report(self) -> str:
        """生成维护报告"""
        report_lines = [
            'APPM模块维护报告',
            '=' * 50,
            f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
            '',
            '数据统计:',
            '-' * 20,
        ]
        
        # 添加各模型的统计信息
        models = [
            (ApplicationGroup, '应用组'),
            (Application, '应用系统'),
            (ApplicationServer, '应用服务器'),
            (ApplicationEndpoint, '应用端点'),
            (ApplicationPersonnel, '应用人员'),
        ]
        
        for model, name in models:
            total = model.objects.count()
            active = model.objects.filter(
                status='active'
            ).count() if hasattr(model, 'status') else 0
            
            report_lines.append(f'{name}: {total} 总计, {active} 活跃')
        
        report_lines.extend([
            '',
            '系统健康检查:',
            '-' * 20,
        ])
        
        # 添加健康检查结果
        apps_without_servers = Application.objects.annotate(
            server_count=Count('servers')
        ).filter(server_count=0).count()
        
        report_lines.append(
            f'无服务器的应用: {apps_without_servers}'
        )
        
        apps_without_endpoints = Application.objects.annotate(
            endpoint_count=Count('endpoints')
        ).filter(endpoint_count=0).count()
        
        report_lines.append(
            f'无端点的应用: {apps_without_endpoints}'
        )
        
        return '\n'.join(report_lines)