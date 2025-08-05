"""APPM模块配置文件

此文件包含APPM模块的配置选项，用于优化性能和自定义行为。
"""

from django.conf import settings

# 默认配置
DEFAULT_CONFIG = {
    # 分页设置
    'PAGINATE_COUNT': 50,
    'MAX_PAGE_SIZE': 1000,
    
    # 缓存设置
    'CACHE_TIMEOUT': 300,  # 5分钟
    'ENABLE_CACHING': True,
    
    # 搜索设置
    'SEARCH_MAX_RESULTS': 100,
    'ENABLE_FULL_TEXT_SEARCH': True,
    
    # 导出设置
    'EXPORT_MAX_RECORDS': 10000,
    'EXPORT_FORMATS': ['csv', 'json', 'yaml'],
    
    # 验证设置
    'STRICT_VALIDATION': True,
    'ENABLE_CUSTOM_VALIDATORS': True,
    
    # 日志设置
    'LOG_LEVEL': 'INFO',
    'ENABLE_AUDIT_LOG': True,
    
    # 性能优化
    'ENABLE_SELECT_RELATED': True,
    'ENABLE_PREFETCH_RELATED': True,
    'BULK_CREATE_BATCH_SIZE': 1000,
    
    # 安全设置
    'ENABLE_PERMISSION_CHECKS': True,
    'REQUIRE_AUTHENTICATION': True,
    
    # 通知设置
    'ENABLE_NOTIFICATIONS': False,
    'NOTIFICATION_CHANNELS': ['email'],
    
    # 集成设置
    'ENABLE_WEBHOOKS': False,
    'WEBHOOK_TIMEOUT': 30,
    
    # 数据保留设置
    'HISTORY_RETENTION_DAYS': 365,
    'CLEANUP_BATCH_SIZE': 1000,
}

# 获取配置值的辅助函数
def get_config(key, default=None):
    """获取APPM配置值
    
    Args:
        key: 配置键名
        default: 默认值
        
    Returns:
        配置值
    """
    appm_config = getattr(settings, 'APPM_CONFIG', {})
    return appm_config.get(key, DEFAULT_CONFIG.get(key, default))

# 常用配置的快捷访问
PAGINATE_COUNT = get_config('PAGINATE_COUNT')
CACHE_TIMEOUT = get_config('CACHE_TIMEOUT')
ENABLE_CACHING = get_config('ENABLE_CACHING')
SEARCH_MAX_RESULTS = get_config('SEARCH_MAX_RESULTS')
EXPORT_MAX_RECORDS = get_config('EXPORT_MAX_RECORDS')
STRICT_VALIDATION = get_config('STRICT_VALIDATION')
ENABLE_SELECT_RELATED = get_config('ENABLE_SELECT_RELATED')
ENABLE_PREFETCH_RELATED = get_config('ENABLE_PREFETCH_RELATED')
BULK_CREATE_BATCH_SIZE = get_config('BULK_CREATE_BATCH_SIZE')

# 数据库查询优化设置
QUERY_OPTIMIZATION = {
    'application_list_select_related': [
        'group',
        'tenant',
        'owner',
    ],
    'application_list_prefetch_related': [
        'servers',
        'endpoints',
        'personnel',
        'tags',
    ],
    'server_list_select_related': [
        'application',
        'application__group',
        'device',
        'virtual_machine',
    ],
    'endpoint_list_select_related': [
        'application',
        'application__group',
        'ip_address',
    ],
    'personnel_list_select_related': [
        'application',
        'application__group',
        'contact',
    ],
}

# 缓存键模板
CACHE_KEYS = {
    'application_list': 'appm:application:list:{hash}',
    'application_detail': 'appm:application:detail:{pk}',
    'server_list': 'appm:server:list:{hash}',
    'server_detail': 'appm:server:detail:{pk}',
    'endpoint_list': 'appm:endpoint:list:{hash}',
    'endpoint_detail': 'appm:endpoint:detail:{pk}',
    'personnel_list': 'appm:personnel:list:{hash}',
    'personnel_detail': 'appm:personnel:detail:{pk}',
    'group_tree': 'appm:group:tree',
    'statistics': 'appm:statistics:{type}',
}

# 搜索配置
SEARCH_CONFIG = {
    'application': {
        'fields': ['name', 'description', 'version'],
        'related_fields': {
            'group__name': 'group_name',
            'tenant__name': 'tenant_name',
            'owner__name': 'owner_name',
        },
        'weight': {
            'name': 3,
            'description': 1,
            'version': 2,
        }
    },
    'server': {
        'fields': ['name', 'description', 'os_name'],
        'related_fields': {
            'application__name': 'application_name',
            'device__name': 'device_name',
            'virtual_machine__name': 'vm_name',
        },
        'weight': {
            'name': 3,
            'description': 1,
            'os_name': 2,
        }
    },
    'endpoint': {
        'fields': ['name', 'description', 'url'],
        'related_fields': {
            'application__name': 'application_name',
        },
        'weight': {
            'name': 3,
            'url': 2,
            'description': 1,
        }
    },
    'personnel': {
        'fields': ['name', 'email', 'department', 'title'],
        'related_fields': {
            'application__name': 'application_name',
            'contact__name': 'contact_name',
        },
        'weight': {
            'name': 3,
            'email': 2,
            'department': 1,
            'title': 1,
        }
    },
}

# 导出配置
EXPORT_CONFIG = {
    'csv': {
        'delimiter': ',',
        'quotechar': '"',
        'encoding': 'utf-8',
    },
    'json': {
        'indent': 2,
        'ensure_ascii': False,
    },
    'yaml': {
        'default_flow_style': False,
        'allow_unicode': True,
    },
}

# 验证规则配置
VALIDATION_CONFIG = {
    'application': {
        'name_max_length': 100,
        'slug_pattern': r'^[a-z0-9-]+$',
        'version_pattern': r'^\d+\.\d+\.\d+$',
        'required_fields': ['name', 'slug'],
    },
    'server': {
        'name_max_length': 100,
        'cpu_cores_max': 128,
        'memory_gb_max': 1024,
        'storage_gb_max': 10240,
        'required_fields': ['name', 'application'],
    },
    'endpoint': {
        'name_max_length': 100,
        'port_range': (1, 65535),
        'url_max_length': 500,
        'required_fields': ['name', 'application'],
    },
    'personnel': {
        'name_max_length': 100,
        'email_max_length': 254,
        'phone_pattern': r'^[+]?[0-9\s\-\(\)]+$',
        'required_fields': ['name', 'application', 'role'],
    },
}

# 权限配置
PERMISSION_CONFIG = {
    'default_permissions': {
        'view': True,
        'add': False,
        'change': False,
        'delete': False,
    },
    'model_permissions': {
        'applicationgroup': ['view', 'add', 'change', 'delete'],
        'application': ['view', 'add', 'change', 'delete'],
        'applicationserver': ['view', 'add', 'change', 'delete'],
        'applicationendpoint': ['view', 'add', 'change', 'delete'],
        'applicationpersonnel': ['view', 'add', 'change', 'delete'],
    },
    'field_permissions': {
        'sensitive_fields': ['password', 'api_key', 'secret'],
        'readonly_fields': ['created', 'last_updated'],
    },
}

# 监控配置
MONITORING_CONFIG = {
    'enable_metrics': True,
    'metrics_retention_days': 30,
    'alert_thresholds': {
        'query_time_ms': 1000,
        'memory_usage_mb': 100,
        'error_rate_percent': 5,
    },
    'health_check_endpoints': [
        '/api/appm/applications/',
        '/api/appm/servers/',
        '/api/appm/endpoints/',
    ],
}

# 集成配置
INTEGRATION_CONFIG = {
    'external_apis': {
        'timeout': 30,
        'retry_count': 3,
        'retry_delay': 1,
    },
    'webhook_config': {
        'max_retries': 3,
        'retry_delay': 5,
        'timeout': 30,
    },
    'sync_config': {
        'batch_size': 100,
        'sync_interval': 3600,  # 1小时
        'enable_auto_sync': False,
    },
}