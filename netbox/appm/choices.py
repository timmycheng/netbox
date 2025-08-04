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
        (STATUS_ACTIVE, 'Active'),
        (STATUS_PLANNED, 'Planned'),
        (STATUS_STAGING, 'Staging'),
        (STATUS_RETIRED, 'Retired'),
        (STATUS_DECOMMISSIONING, 'Decommissioning'),
    ]


class ApplicationCriticalityChoices(ChoiceSet):
    key = 'Application.criticality'

    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'

    CHOICES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (CRITICAL, 'Critical'),
    ]


class ApplicationEnvironmentChoices(ChoiceSet):
    key = 'Application.environment'

    DEVELOPMENT = 'development'
    TESTING = 'testing'
    STAGING = 'staging'
    PRODUCTION = 'production'
    DISASTER_RECOVERY = 'disaster_recovery'

    CHOICES = [
        (DEVELOPMENT, 'Development'),
        (TESTING, 'Testing'),
        (STAGING, 'Staging'),
        (PRODUCTION, 'Production'),
        (DISASTER_RECOVERY, 'Disaster Recovery'),
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
        (STATUS_ACTIVE, 'Active'),
        (STATUS_PLANNED, 'Planned'),
        (STATUS_OFFLINE, 'Offline'),
        (STATUS_DECOMMISSIONING, 'Decommissioning'),
        (STATUS_FAILED, 'Failed'),
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
        (WEB_SERVER, 'Web Server'),
        (APPLICATION_SERVER, 'Application Server'),
        (DATABASE_SERVER, 'Database Server'),
        (CACHE_SERVER, 'Cache Server'),
        (LOAD_BALANCER, 'Load Balancer'),
        (FILE_SERVER, 'File Server'),
        (BACKUP_SERVER, 'Backup Server'),
        (MONITORING_SERVER, 'Monitoring Server'),
        (OTHER, 'Other'),
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
        (STATUS_ACTIVE, 'Active'),
        (STATUS_PLANNED, 'Planned'),
        (STATUS_MAINTENANCE, 'Maintenance'),
        (STATUS_DEPRECATED, 'Deprecated'),
        (STATUS_DISABLED, 'Disabled'),
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
        (WEB_UI, 'Web UI'),
        (API, 'API'),
        (WEB_SERVICE, 'Web Service'),
        (DATABASE, 'Database'),
        (FTP, 'FTP'),
        (SSH, 'SSH'),
        (OTHER, 'Other'),
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
        (OWNER, 'Owner'),
        (DEVELOPER, 'Developer'),
        (ADMINISTRATOR, 'Administrator'),
        (OPERATOR, 'Operator'),
        (BUSINESS_ANALYST, 'Business Analyst'),
        (PROJECT_MANAGER, 'Project Manager'),
        (ARCHITECT, 'Architect'),
        (TESTER, 'Tester'),
        (SUPPORT, 'Support'),
        (OTHER, 'Other'),
    ]