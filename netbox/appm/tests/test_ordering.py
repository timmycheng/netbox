from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant, Contact
from virtualization.models import VirtualMachine, Cluster, ClusterType
from appm.choices import *
from appm.models import *
from utilities.testing import TestCase as UtilitiesTestCase


class ApplicationGroupOrderingTest(TestCase):
    """测试ApplicationGroup模型的排序功能"""

    @classmethod
    def setUpTestData(cls):
        ApplicationGroup.objects.bulk_create([
            ApplicationGroup(name='Zebra Applications', slug='zebra-applications'),
            ApplicationGroup(name='Alpha Applications', slug='alpha-applications'),
            ApplicationGroup(name='Beta Applications', slug='beta-applications'),
        ])

    def test_default_ordering(self):
        """测试默认按名称排序"""
        groups = list(ApplicationGroup.objects.all())
        names = [group.name for group in groups]
        self.assertEqual(names, ['Alpha Applications', 'Beta Applications', 'Zebra Applications'])

    def test_ordering_by_slug(self):
        """测试按slug排序"""
        groups = list(ApplicationGroup.objects.order_by('slug'))
        slugs = [group.slug for group in groups]
        self.assertEqual(slugs, ['alpha-applications', 'beta-applications', 'zebra-applications'])

    def test_reverse_ordering(self):
        """测试反向排序"""
        groups = list(ApplicationGroup.objects.order_by('-name'))
        names = [group.name for group in groups]
        self.assertEqual(names, ['Zebra Applications', 'Beta Applications', 'Alpha Applications'])


class ApplicationOrderingTest(TestCase):
    """测试Application模型的排序功能"""

    @classmethod
    def setUpTestData(cls):
        group = ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group'
        )
        
        Application.objects.bulk_create([
            Application(
                name='Zebra App',
                slug='zebra-app',
                group=group,
                environment=ApplicationEnvironmentChoices.PRODUCTION,
                criticality=ApplicationCriticalityChoices.HIGH
            ),
            Application(
                name='Alpha App',
                slug='alpha-app',
                group=group,
                environment=ApplicationEnvironmentChoices.STAGING,
                criticality=ApplicationCriticalityChoices.LOW
            ),
            Application(
                name='Beta App',
                slug='beta-app',
                group=group,
                environment=ApplicationEnvironmentChoices.DEVELOPMENT,
                criticality=ApplicationCriticalityChoices.MEDIUM
            ),
        ])

    def test_default_ordering(self):
        """测试默认按名称排序"""
        apps = list(Application.objects.all())
        names = [app.name for app in apps]
        self.assertEqual(names, ['Alpha App', 'Beta App', 'Zebra App'])

    def test_ordering_by_environment(self):
        """测试按环境排序"""
        apps = list(Application.objects.order_by('environment'))
        environments = [app.environment for app in apps]
        self.assertEqual(environments, [
            ApplicationEnvironmentChoices.DEVELOPMENT,
            ApplicationEnvironmentChoices.PRODUCTION,
            ApplicationEnvironmentChoices.STAGING
        ])

    def test_ordering_by_criticality(self):
        """测试按重要性排序"""
        apps = list(Application.objects.order_by('criticality'))
        criticalities = [app.criticality for app in apps]
        self.assertEqual(criticalities, [
            ApplicationCriticalityChoices.HIGH,
            ApplicationCriticalityChoices.LOW,
            ApplicationCriticalityChoices.MEDIUM
        ])

    def test_multiple_field_ordering(self):
        """测试多字段排序"""
        apps = list(Application.objects.order_by('environment', 'name'))
        # 按环境和名称排序
        expected_order = [
            ('Beta App', ApplicationEnvironmentChoices.DEVELOPMENT),
            ('Zebra App', ApplicationEnvironmentChoices.PRODUCTION),
            ('Alpha App', ApplicationEnvironmentChoices.STAGING),
        ]
        actual_order = [(app.name, app.environment) for app in apps]
        self.assertEqual(actual_order, expected_order)


class ApplicationServerOrderingTest(TestCase):
    """测试ApplicationServer模型的排序功能"""

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统
        group = ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group'
        )
        cls.app1 = Application.objects.create(
            name='App 1',
            slug='app-1',
            group=group,
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        cls.app2 = Application.objects.create(
            name='App 2',
            slug='app-2',
            group=group,
            environment=ApplicationEnvironmentChoices.STAGING
        )
        
        # 创建设备
        manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
            slug='test-manufacturer'
        )
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model='Test Model',
            slug='test-model'
        )
        device_role = DeviceRole.objects.create(
            name='Server',
            slug='server'
        )
        site = Site.objects.create(
            name='Test Site',
            slug='test-site'
        )
        device = Device.objects.create(
            name='test-device',
            device_type=device_type,
            role=device_role,
            site=site
        )
        
        # 创建应用服务器
        ApplicationServer.objects.bulk_create([
            ApplicationServer(
                application=cls.app1,
                device=device,
                name='Zebra Server',
                role=ServerRoleChoices.WEB_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE
            ),
            ApplicationServer(
                application=cls.app1,
                device=device,
                name='Alpha Server',
                role=ServerRoleChoices.DATABASE_SERVER,
                status=ServerStatusChoices.STATUS_PLANNED
            ),
            ApplicationServer(
                application=cls.app2,
                device=device,
                name='Beta Server',
                role=ServerRoleChoices.APPLICATION_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE
            ),
        ])

    def test_default_ordering(self):
        """测试默认按应用系统和名称排序"""
        servers = list(ApplicationServer.objects.all())
        expected_order = [
            ('App 1', 'Alpha Server'),
            ('App 1', 'Zebra Server'),
            ('App 2', 'Beta Server'),
        ]
        actual_order = [(server.application.name, server.name) for server in servers]
        self.assertEqual(actual_order, expected_order)

    def test_ordering_by_role(self):
        """测试按角色排序"""
        servers = list(ApplicationServer.objects.order_by('role'))
        roles = [server.role for server in servers]
        self.assertEqual(roles, [
            ServerRoleChoices.APPLICATION_SERVER,
            ServerRoleChoices.DATABASE_SERVER,
            ServerRoleChoices.WEB_SERVER
        ])

    def test_ordering_by_status(self):
        """测试按状态排序"""
        servers = list(ApplicationServer.objects.order_by('status'))
        statuses = [server.status for server in servers]
        self.assertEqual(statuses, [
            ServerStatusChoices.STATUS_ACTIVE,
            ServerStatusChoices.STATUS_ACTIVE,
            ServerStatusChoices.STATUS_PLANNED
        ])


class ApplicationEndpointOrderingTest(TestCase):
    """测试ApplicationEndpoint模型的排序功能"""

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统和服务器
        group = ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group'
        )
        cls.app1 = Application.objects.create(
            name='App 1',
            slug='app-1',
            group=group,
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        cls.app2 = Application.objects.create(
            name='App 2',
            slug='app-2',
            group=group,
            environment=ApplicationEnvironmentChoices.STAGING
        )
        
        # 创建设备和服务器
        manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
            slug='test-manufacturer'
        )
        device_type = DeviceType.objects.create(
            manufacturer=manufacturer,
            model='Test Model',
            slug='test-model'
        )
        device_role = DeviceRole.objects.create(
            name='Server',
            slug='server'
        )
        site = Site.objects.create(
            name='Test Site',
            slug='test-site'
        )
        device = Device.objects.create(
            name='test-device',
            device_type=device_type,
            role=device_role,
            site=site
        )
        
        server = ApplicationServer.objects.create(
            application=cls.app1,
            device=device,
            name='Test Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        
        # 创建应用端点
        ApplicationEndpoint.objects.bulk_create([
            ApplicationEndpoint(
                application=cls.app1,
                server=server,
                name='Zebra Endpoint',
                type=EndpointTypeChoices.WEB_UI,
                status=EndpointStatusChoices.STATUS_ACTIVE
            ),
            ApplicationEndpoint(
                application=cls.app1,
                server=server,
                name='Alpha Endpoint',
                type=EndpointTypeChoices.API,
                status=EndpointStatusChoices.STATUS_PLANNED
            ),
            ApplicationEndpoint(
                application=cls.app2,
                server=server,
                name='Beta Endpoint',
                type=EndpointTypeChoices.DATABASE,
                status=EndpointStatusChoices.STATUS_ACTIVE
            ),
        ])

    def test_default_ordering(self):
        """测试默认按应用系统和名称排序"""
        endpoints = list(ApplicationEndpoint.objects.all())
        expected_order = [
            ('App 1', 'Alpha Endpoint'),
            ('App 1', 'Zebra Endpoint'),
            ('App 2', 'Beta Endpoint'),
        ]
        actual_order = [(endpoint.application.name, endpoint.name) for endpoint in endpoints]
        self.assertEqual(actual_order, expected_order)

    def test_ordering_by_type(self):
        """测试按类型排序"""
        endpoints = list(ApplicationEndpoint.objects.order_by('type'))
        types = [endpoint.type for endpoint in endpoints]
        self.assertEqual(types, [
            EndpointTypeChoices.API,
            EndpointTypeChoices.DATABASE,
            EndpointTypeChoices.WEB_UI
        ])

    def test_ordering_by_status(self):
        """测试按状态排序"""
        endpoints = list(ApplicationEndpoint.objects.order_by('status'))
        statuses = [endpoint.status for endpoint in endpoints]
        self.assertEqual(statuses, [
            EndpointStatusChoices.STATUS_ACTIVE,
            EndpointStatusChoices.STATUS_ACTIVE,
            EndpointStatusChoices.STATUS_PLANNED
        ])


class ApplicationPersonnelOrderingTest(TestCase):
    """测试ApplicationPersonnel模型的排序功能"""

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统
        group = ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group'
        )
        cls.app1 = Application.objects.create(
            name='App 1',
            slug='app-1',
            group=group,
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        cls.app2 = Application.objects.create(
            name='App 2',
            slug='app-2',
            group=group,
            environment=ApplicationEnvironmentChoices.STAGING
        )
        
        # 创建联系人
        contact = Contact.objects.create(
            name='Test Contact',
            email='test@example.com'
        )
        
        # 创建应用人员
        ApplicationPersonnel.objects.bulk_create([
            ApplicationPersonnel(
                application=cls.app1,
                contact=contact,
                name='Zebra Person',
                role=PersonnelRoleChoices.OWNER
            ),
            ApplicationPersonnel(
                application=cls.app1,
                contact=contact,
                name='Alpha Person',
                role=PersonnelRoleChoices.DEVELOPER
            ),
            ApplicationPersonnel(
                application=cls.app2,
                contact=contact,
                name='Beta Person',
                role=PersonnelRoleChoices.ADMINISTRATOR
            ),
            ApplicationPersonnel(
                application=cls.app1,
                contact=contact,
                name='Charlie Person',
                role=PersonnelRoleChoices.OWNER  # 同一应用系统，同一角色，不同人员
            ),
        ])

    def test_default_ordering(self):
        """测试默认按应用系统、角色和名称排序"""
        personnel = list(ApplicationPersonnel.objects.all())
        expected_order = [
            ('App 1', PersonnelRoleChoices.DEVELOPER, 'Alpha Person'),
            ('App 1', PersonnelRoleChoices.OWNER, 'Charlie Person'),
            ('App 1', PersonnelRoleChoices.OWNER, 'Zebra Person'),
            ('App 2', PersonnelRoleChoices.ADMINISTRATOR, 'Beta Person'),
        ]
        actual_order = [(p.application.name, p.role, p.name) for p in personnel]
        self.assertEqual(actual_order, expected_order)

    def test_ordering_by_role_only(self):
        """测试仅按角色排序"""
        personnel = list(ApplicationPersonnel.objects.order_by('role'))
        roles = [p.role for p in personnel]
        self.assertEqual(roles, [
            PersonnelRoleChoices.ADMINISTRATOR,
            PersonnelRoleChoices.DEVELOPER,
            PersonnelRoleChoices.OWNER,
            PersonnelRoleChoices.OWNER
        ])

    def test_ordering_by_name_only(self):
        """测试仅按名称排序"""
        personnel = list(ApplicationPersonnel.objects.order_by('name'))
        names = [p.name for p in personnel]
        self.assertEqual(names, ['Alpha Person', 'Beta Person', 'Charlie Person', 'Zebra Person'])

    def test_reverse_ordering(self):
        """测试反向排序"""
        personnel = list(ApplicationPersonnel.objects.order_by('-name'))
        names = [p.name for p in personnel]
        self.assertEqual(names, ['Zebra Person', 'Charlie Person', 'Beta Person', 'Alpha Person'])