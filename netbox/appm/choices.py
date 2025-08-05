from django.utils.translation import gettext_lazy as _
from utilities.choices import ChoiceSet


#
# Application choices
#

class ApplicationStatusChoices(ChoiceSet):
    key = 'Application.status'

    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_STAGING = 'staging'
    STATUS_RETIRED = 'retired'
    STATUS_DECOMMISSIONING = 'decommissioning'

    CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_PLANNED, _('Planned')),
        (STATUS_STAGING, _('Staging')),
        (STATUS_RETIRED, _('Retired')),
        (STATUS_DECOMMISSIONING, _('Decommissioning')),
    ]


class ApplicationCriticalityChoices(ChoiceSet):
    key = 'Application.criticality'

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

    CHOICES = [
        (LOW, _('Low')),
        (MEDIUM, _('Medium')),
        (HIGH, _('High')),
        (CRITICAL, _('Critical')),
    ]


class ApplicationEnvironmentChoices(ChoiceSet):
    key = 'Application.environment'

    DEVELOPMENT = 'development'
    TESTING = 'testing'
    STAGING = 'staging'
    PRODUCTION = 'production'
    DISASTER_RECOVERY = 'disaster_recovery'

    CHOICES = [
        (DEVELOPMENT, _('Development')),
        (TESTING, _('Testing')),
        (STAGING, _('Staging')),
        (PRODUCTION, _('Production')),
        (DISASTER_RECOVERY, _('Disaster Recovery')),
    ]


#
# Server choices
#

class ServerStatusChoices(ChoiceSet):
    key = 'Server.status'

    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_OFFLINE = 'offline'
    STATUS_DECOMMISSIONING = 'decommissioning'
    STATUS_FAILED = 'failed'

    CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_PLANNED, _('Planned')),
        (STATUS_OFFLINE, _('Offline')),
        (STATUS_DECOMMISSIONING, _('Decommissioning')),
        (STATUS_FAILED, _('Failed')),
    ]


class ServerRoleChoices(ChoiceSet):
    key = 'Server.role'

    WEB_SERVER = 'web_server'
    APPLICATION_SERVER = 'application_server'
    DATABASE_SERVER = 'database_server'
    CACHE_SERVER = 'cache_server'
    LOAD_BALANCER = 'load_balancer'
    FILE_SERVER = 'file_server'
    BACKUP_SERVER = 'backup_server'
    MONITORING_SERVER = 'monitoring_server'
    OTHER = 'other'

    CHOICES = [
        (WEB_SERVER, _('Web Server')),
        (APPLICATION_SERVER, _('Application Server')),
        (DATABASE_SERVER, _('Database Server')),
        (CACHE_SERVER, _('Cache Server')),
        (LOAD_BALANCER, _('Load Balancer')),
        (FILE_SERVER, _('File Server')),
        (BACKUP_SERVER, _('Backup Server')),
        (MONITORING_SERVER, _('Monitoring Server')),
        (OTHER, _('Other')),
    ]


#
# Endpoint choices
#

class EndpointStatusChoices(ChoiceSet):
    key = 'Endpoint.status'

    STATUS_ACTIVE = 'active'
    STATUS_PLANNED = 'planned'
    STATUS_MAINTENANCE = 'maintenance'
    STATUS_DEPRECATED = 'deprecated'
    STATUS_DISABLED = 'disabled'

    CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_PLANNED, _('Planned')),
        (STATUS_MAINTENANCE, _('Maintenance')),
        (STATUS_DEPRECATED, _('Deprecated')),
        (STATUS_DISABLED, _('Disabled')),
    ]


class EndpointTypeChoices(ChoiceSet):
    key = 'Endpoint.type'

    WEB_UI = 'web_ui'
    API = 'api'
    WEB_SERVICE = 'web_service'
    DATABASE = 'database'
    FTP = 'ftp'
    SSH = 'ssh'
    OTHER = 'other'

    CHOICES = [
        (WEB_UI, _('Web UI')),
        (API, _('API')),
        (WEB_SERVICE, _('Web Service')),
        (DATABASE, _('Database')),
        (FTP, _('FTP')),
        (SSH, _('SSH')),
        (OTHER, _('Other')),
    ]


#
# Personnel choices
#

class PersonnelRoleChoices(ChoiceSet):
    key = 'Personnel.role'

    OWNER = 'owner'
    DEVELOPER = 'developer'
    ADMINISTRATOR = 'administrator'
    OPERATOR = 'operator'
    BUSINESS_ANALYST = 'business_analyst'
    PROJECT_MANAGER = 'project_manager'
    ARCHITECT = 'architect'
    TESTER = 'tester'
    SUPPORT = 'support'
    OTHER = 'other'

    CHOICES = [
        (OWNER, _('Owner')),
        (DEVELOPER, _('Developer')),
        (ADMINISTRATOR, _('Administrator')),
        (OPERATOR, _('Operator')),
        (BUSINESS_ANALYST, _('Business Analyst')),
        (PROJECT_MANAGER, _('Project Manager')),
        (ARCHITECT, _('Architect')),
        (TESTER, _('Tester')),
        (SUPPORT, _('Support')),
        (OTHER, _('Other')),
    ]