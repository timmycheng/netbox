"""APPM模块工具函数

此文件包含APPM模块使用的各种工具函数和辅助类。
"""

import re
import hashlib
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta

from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.db.models import QuerySet, Q, Count
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .config import get_config, CACHE_KEYS, CACHE_TIMEOUT

logger = logging.getLogger(__name__)


class APPMCache:
    """APPM缓存管理器"""
    
    @staticmethod
    def get_cache_key(template: str, **kwargs) -> str:
        """生成缓存键
        
        Args:
            template: 缓存键模板
            **kwargs: 模板参数
            
        Returns:
            生成的缓存键
        """
        return template.format(**kwargs)
    
    @staticmethod
    def get_list_cache_key(model_name: str, filters: Dict) -> str:
        """生成列表缓存键
        
        Args:
            model_name: 模型名称
            filters: 过滤条件
            
        Returns:
            缓存键
        """
        filter_hash = hashlib.md5(
            str(sorted(filters.items())).encode('utf-8')
        ).hexdigest()[:8]
        
        template = CACHE_KEYS.get(f'{model_name}_list', 'appm:{model}:list:{hash}')
        return template.format(model=model_name, hash=filter_hash)
    
    @staticmethod
    def get_detail_cache_key(model_name: str, pk: int) -> str:
        """生成详情缓存键
        
        Args:
            model_name: 模型名称
            pk: 主键
            
        Returns:
            缓存键
        """
        template = CACHE_KEYS.get(f'{model_name}_detail', 'appm:{model}:detail:{pk}')
        return template.format(model=model_name, pk=pk)
    
    @staticmethod
    def set_cache(key: str, value: Any, timeout: Optional[int] = None) -> None:
        """设置缓存
        
        Args:
            key: 缓存键
            value: 缓存值
            timeout: 超时时间（秒）
        """
        if not get_config('ENABLE_CACHING'):
            return
            
        timeout = timeout or CACHE_TIMEOUT
        cache.set(key, value, timeout)
        logger.debug(f"Cache set: {key} (timeout: {timeout}s)")
    
    @staticmethod
    def get_cache(key: str, default: Any = None) -> Any:
        """获取缓存
        
        Args:
            key: 缓存键
            default: 默认值
            
        Returns:
            缓存值或默认值
        """
        if not get_config('ENABLE_CACHING'):
            return default
            
        value = cache.get(key, default)
        logger.debug(f"Cache get: {key} ({'hit' if value != default else 'miss'})")
        return value
    
    @staticmethod
    def delete_cache(key: str) -> None:
        """删除缓存
        
        Args:
            key: 缓存键
        """
        cache.delete(key)
        logger.debug(f"Cache deleted: {key}")
    
    @staticmethod
    def clear_model_cache(model_name: str) -> None:
        """清除模型相关的所有缓存
        
        Args:
            model_name: 模型名称
        """
        # 这里可以实现更复杂的缓存清理逻辑
        # 由于Django缓存API限制，这里只是示例
        logger.info(f"Clearing cache for model: {model_name}")


class QueryOptimizer:
    """查询优化器"""
    
    @staticmethod
    def optimize_queryset(queryset: QuerySet, model_name: str, 
                         operation: str = 'list') -> QuerySet:
        """优化查询集
        
        Args:
            queryset: 原始查询集
            model_name: 模型名称
            operation: 操作类型（list/detail）
            
        Returns:
            优化后的查询集
        """
        from .config import QUERY_OPTIMIZATION
        
        if not get_config('ENABLE_SELECT_RELATED'):
            return queryset
            
        # 应用select_related优化
        select_related_key = f'{model_name}_{operation}_select_related'
        select_related = QUERY_OPTIMIZATION.get(select_related_key, [])
        if select_related:
            queryset = queryset.select_related(*select_related)
            
        # 应用prefetch_related优化
        if get_config('ENABLE_PREFETCH_RELATED'):
            prefetch_related_key = f'{model_name}_{operation}_prefetch_related'
            prefetch_related = QUERY_OPTIMIZATION.get(prefetch_related_key, [])
            if prefetch_related:
                queryset = queryset.prefetch_related(*prefetch_related)
                
        return queryset


class SearchHelper:
    """搜索辅助类"""
    
    @staticmethod
    def build_search_query(model_name: str, search_term: str) -> Q:
        """构建搜索查询
        
        Args:
            model_name: 模型名称
            search_term: 搜索词
            
        Returns:
            Django Q对象
        """
        from .config import SEARCH_CONFIG
        
        config = SEARCH_CONFIG.get(model_name, {})
        fields = config.get('fields', [])
        related_fields = config.get('related_fields', {})
        
        query = Q()
        
        # 搜索主要字段
        for field in fields:
            query |= Q(**{f'{field}__icontains': search_term})
            
        # 搜索关联字段
        for field, alias in related_fields.items():
            query |= Q(**{f'{field}__icontains': search_term})
            
        return query
    
    @staticmethod
    def highlight_search_term(text: str, search_term: str) -> str:
        """高亮搜索词
        
        Args:
            text: 原始文本
            search_term: 搜索词
            
        Returns:
            高亮后的文本
        """
        if not search_term or not text:
            return text
            
        pattern = re.compile(re.escape(search_term), re.IGNORECASE)
        return pattern.sub(f'<mark>{search_term}</mark>', text)


class ValidationHelper:
    """验证辅助类"""
    
    @staticmethod
    def validate_slug(slug: str, model_name: str = None) -> None:
        """验证slug格式
        
        Args:
            slug: slug值
            model_name: 模型名称（用于获取特定验证规则）
            
        Raises:
            ValidationError: 验证失败时抛出
        """
        from .config import VALIDATION_CONFIG
        
        if not slug:
            raise ValidationError(_("Slug不能为空"))
            
        # 获取模型特定的验证规则
        config = VALIDATION_CONFIG.get(model_name, {}) if model_name else {}
        pattern = config.get('slug_pattern', r'^[a-z0-9-]+$')
        
        if not re.match(pattern, slug):
            raise ValidationError(_("Slug格式无效，只能包含小写字母、数字和连字符"))
    
    @staticmethod
    def validate_version(version: str) -> None:
        """验证版本号格式
        
        Args:
            version: 版本号
            
        Raises:
            ValidationError: 验证失败时抛出
        """
        if not version:
            return
            
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$'
        if not re.match(pattern, version):
            raise ValidationError(_("版本号格式无效，应为 x.y.z 或 x.y.z-suffix 格式"))
    
    @staticmethod
    def validate_port(port: int) -> None:
        """验证端口号
        
        Args:
            port: 端口号
            
        Raises:
            ValidationError: 验证失败时抛出
        """
        if port is None:
            return
            
        if not (1 <= port <= 65535):
            raise ValidationError(_("端口号必须在1-65535范围内"))
    
    @staticmethod
    def validate_email(email: str) -> None:
        """验证邮箱格式
        
        Args:
            email: 邮箱地址
            
        Raises:
            ValidationError: 验证失败时抛出
        """
        if not email:
            return
            
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError(_("邮箱格式无效"))
    
    @staticmethod
    def validate_phone(phone: str) -> None:
        """验证电话号码格式
        
        Args:
            phone: 电话号码
            
        Raises:
            ValidationError: 验证失败时抛出
        """
        if not phone:
            return
            
        # 移除所有空格和特殊字符进行验证
        clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not clean_phone.isdigit() or len(clean_phone) < 7:
            raise ValidationError(_("电话号码格式无效"))


class ExportHelper:
    """导出辅助类"""
    
    @staticmethod
    def prepare_export_data(queryset: QuerySet, fields: List[str]) -> List[Dict]:
        """准备导出数据
        
        Args:
            queryset: 查询集
            fields: 要导出的字段列表
            
        Returns:
            导出数据列表
        """
        data = []
        max_records = get_config('EXPORT_MAX_RECORDS')
        
        for i, obj in enumerate(queryset):
            if i >= max_records:
                logger.warning(f"Export limited to {max_records} records")
                break
                
            row = {}
            for field in fields:
                value = getattr(obj, field, None)
                if hasattr(value, 'all'):  # Many-to-many field
                    value = ', '.join(str(v) for v in value.all())
                elif hasattr(value, '__str__'):
                    value = str(value)
                row[field] = value
            data.append(row)
            
        return data
    
    @staticmethod
    def get_export_filename(model_name: str, format_type: str) -> str:
        """生成导出文件名
        
        Args:
            model_name: 模型名称
            format_type: 格式类型
            
        Returns:
            文件名
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f'{model_name}_{timestamp}.{format_type}'


class PermissionHelper:
    """权限辅助类"""
    
    @staticmethod
    def check_model_permission(user, model_name: str, action: str) -> bool:
        """检查模型权限
        
        Args:
            user: 用户对象
            model_name: 模型名称
            action: 操作类型（view/add/change/delete）
            
        Returns:
            是否有权限
        """
        if not get_config('ENABLE_PERMISSION_CHECKS'):
            return True
            
        if user.is_superuser:
            return True
            
        permission_name = f'appm.{action}_{model_name}'
        return user.has_perm(permission_name)
    
    @staticmethod
    def filter_sensitive_fields(data: Dict, user) -> Dict:
        """过滤敏感字段
        
        Args:
            data: 原始数据
            user: 用户对象
            
        Returns:
            过滤后的数据
        """
        from .config import PERMISSION_CONFIG
        
        if user.is_superuser:
            return data
            
        sensitive_fields = PERMISSION_CONFIG.get('field_permissions', {}).get('sensitive_fields', [])
        filtered_data = data.copy()
        
        for field in sensitive_fields:
            if field in filtered_data:
                filtered_data[field] = '***'
                
        return filtered_data


class StatisticsHelper:
    """统计辅助类"""
    
    @staticmethod
    def get_model_statistics(model_class) -> Dict[str, int]:
        """获取模型统计信息
        
        Args:
            model_class: 模型类
            
        Returns:
            统计信息字典
        """
        cache_key = APPMCache.get_cache_key(
            CACHE_KEYS['statistics'], 
            type=model_class._meta.model_name
        )
        
        stats = APPMCache.get_cache(cache_key)
        if stats is not None:
            return stats
            
        stats = {
            'total': model_class.objects.count(),
            'active': model_class.objects.filter(
                status='active'
            ).count() if hasattr(model_class, 'status') else 0,
        }
        
        # 添加特定模型的统计
        if hasattr(model_class, 'environment'):
            stats['by_environment'] = dict(
                model_class.objects.values_list('environment')
                .annotate(count=Count('id'))
            )
            
        APPMCache.set_cache(cache_key, stats, 300)  # 缓存5分钟
        return stats


class SlugHelper:
    """Slug辅助类"""
    
    @staticmethod
    def generate_unique_slug(name: str, model_class, instance=None) -> str:
        """生成唯一的slug
        
        Args:
            name: 名称
            model_class: 模型类
            instance: 实例（用于更新时排除自身）
            
        Returns:
            唯一的slug
        """
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        
        while True:
            queryset = model_class.objects.filter(slug=slug)
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
                
            if not queryset.exists():
                break
                
            slug = f'{base_slug}-{counter}'
            counter += 1
            
        return slug


class DateHelper:
    """日期辅助类"""
    
    @staticmethod
    def get_date_range(period: str) -> tuple:
        """获取日期范围
        
        Args:
            period: 时间段（today/week/month/year）
            
        Returns:
            (开始日期, 结束日期)
        """
        now = datetime.now()
        
        if period == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == 'week':
            start = now - timedelta(days=7)
            end = now
        elif period == 'month':
            start = now - timedelta(days=30)
            end = now
        elif period == 'year':
            start = now - timedelta(days=365)
            end = now
        else:
            start = end = now
            
        return start, end
    
    @staticmethod
    def format_duration(seconds: int) -> str:
        """格式化持续时间
        
        Args:
            seconds: 秒数
            
        Returns:
            格式化的时间字符串
        """
        if seconds < 60:
            return f"{seconds}秒"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}分钟"
        elif seconds < 86400:
            hours = seconds // 3600
            return f"{hours}小时"
        else:
            days = seconds // 86400
            return f"{days}天"


# 常用装饰器
def cache_result(timeout: int = None):
    """缓存结果装饰器
    
    Args:
        timeout: 缓存超时时间
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not get_config('ENABLE_CACHING'):
                return func(*args, **kwargs)
                
            # 生成缓存键
            cache_key = f"appm:func:{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # 尝试从缓存获取
            result = APPMCache.get_cache(cache_key)
            if result is not None:
                return result
                
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            APPMCache.set_cache(cache_key, result, timeout or CACHE_TIMEOUT)
            return result
            
        return wrapper
    return decorator


def log_execution_time(func):
    """记录执行时间装饰器"""
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        
        execution_time = (end_time - start_time).total_seconds()
        logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
        
        return result
    return wrapper