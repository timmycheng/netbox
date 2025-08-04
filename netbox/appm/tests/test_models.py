from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant, Contact
from virtualization.models import VirtualMachine, Cluster, ClusterType
from appm.choices import *
from appm.models import *


class TestApplicationGroup(TestCase):

    def test_create_application_group(self):
        """测试创建应用系统分组"""
        group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications',
            description='Web application group'
        )
        self.assertEqual(group.name, 'Web Applications')
        self.assertEqual(group.slug, 'web-applications')
        self.assertEqual(str(group), 'Web Applications')

    def test_unique_name_per_parent(self):
        """测试应用系统分组在同一父级下名称唯一性"""
        parent = ApplicationGroup.objects.create(
            name='Parent Group',
            slug='parent-group'
        )
        ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group',
            parent=parent
        )
        with self.assertRaises(Exception):
            ApplicationGroup.objects.create(
                name='Test Group',
                slug='test-group-2',
                parent=parent
            )

    def test_different_parents_same_name(self):
        """测试不同父级下可以有相同名称的分组"""
        parent1 = ApplicationGroup.objects.create(
            name='Parent Group 1',
            slug='parent-group-1'
        )
        parent2 = ApplicationGroup.objects.create(
            name='Parent Group 2',
            slug='parent-group-2'
        )
        # 不同父级下可以有相同名称
        group1 = ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group-1',
            parent=parent1
        )
        group2 = ApplicationGroup.objects.create(
            name='Test Group',
            slug='test-group-2',
            parent=parent2
        )
        self.assertEqual(group1.name, group2.name)
        self.assertNotEqual(group1.parent, group2.parent)


class TestApplication(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        cls.tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant'
        )

    def test_create_application(self):
        """测试创建应用系统"""
        app = Application.objects.create(
            name='Test App',
            slug='test-app',
            group=self.group,
            status=ApplicationStatusChoices.STATUS_ACTIVE,
            tenant=self.tenant,
            version='1.0.0',
            owner='John Doe',
            business_unit='IT Department',
            criticality=ApplicationCriticalityChoices.HIGH,
            environment=ApplicationEnvironmentChoices.PRODUCTION,
            description='Test application'
        )
        self.assertEqual(app.name, 'Test App')
        self.assertEqual(app.slug, 'test-app')
        self.assertEqual(app.group, self.group)
        self.assertEqual(app.status, ApplicationStatusChoices.STATUS_ACTIVE)
        self.assertEqual(app.tenant, self.tenant)
        self.assertEqual(app.version, '1.0.0')
        self.assertEqual(app.owner, 'John Doe')
        self.assertEqual(app.business_unit, 'IT Department')
        self.assertEqual(app.criticality, ApplicationCriticalityChoices.HIGH)
        self.assertEqual(app.environment, ApplicationEnvironmentChoices.PRODUCTION)
        self.assertEqual(str(app), 'Test App')

    def test_unique_name_environment(self):
        """测试应用系统名称和环境的唯一性约束"""
        Application.objects.create(
            name='Test App',
            slug='test-app-prod',
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        with self.assertRaises(Exception):
            Application.objects.create(
                name='Test App',
                slug='test-app-prod-2',
                environment=ApplicationEnvironmentChoices.PRODUCTION
            )

    def test_different_environments_allowed(self):
        """测试相同名称的应用系统在不同环境下可以创建"""
        Application.objects.create(
            name='Test App',
            slug='test-app-prod',
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        app_staging = Application.objects.create(
            name='Test App',
            slug='test-app-staging',
            environment=ApplicationEnvironmentChoices.STAGING
        )
        self.assertEqual(app_staging.name, 'Test App')
        self.assertEqual(app_staging.environment, ApplicationEnvironmentChoices.STAGING)

    def test_get_status_color(self):
        """测试获取状态颜色"""
        app = Application.objects.create(
            name='Test App',
            slug='test-app',
            status=ApplicationStatusChoices.STATUS_ACTIVE
        )
        color = app.get_status_color()
        self.assertIsNotNone(color)


class TestApplicationServer(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(
            name='Test App',
            slug='test-app'
        )
        
        # 创建设备相关对象
        cls.manufacturer = Manufacturer.objects.create(
            name='Test Manufacturer',
            slug='test-manufacturer'
        )
        cls.device_type = DeviceType.objects.create(
            manufacturer=cls.manufacturer,
            model='Test Model',
            slug='test-model'
        )
        cls.device_role = DeviceRole.objects.create(
            name='Server',
            slug='server'
        )
        cls.site = Site.objects.create(
            name='Test Site',
            slug='test-site'
        )
        cls.device = Device.objects.create(
            name='test-device',
            device_type=cls.device_type,
            role=cls.device_role,
            site=cls.site
        )
        
        # 创建虚拟机相关对象
        cls.cluster_type = ClusterType.objects.create(
            name='Test Cluster Type',
            slug='test-cluster-type'
        )
        cls.cluster = Cluster.objects.create(
            name='Test Cluster',
            type=cls.cluster_type
        )
        cls.virtual_machine = VirtualMachine.objects.create(
            name='test-vm',
            cluster=cls.cluster
        )
        
        # 创建IP地址
        cls.ip_address = IPAddress.objects.create(
            address='192.168.1.100/24'
        )

    def test_create_application_server_with_device(self):
        """测试创建关联物理设备的应用服务器"""
        server = ApplicationServer.objects.create(
            application=self.application,
            device=self.device,
            name='Web Server 1',
            role=ServerRoleChoices.WEB_SERVER,
            status=ServerStatusChoices.STATUS_ACTIVE,
            primary_ip4=self.ip_address,
            cpu_cores=4,
            memory_gb=8,
            storage_gb=100,
            operating_system='Ubuntu 20.04',
            middleware='Apache, PHP',
            description='Primary web server'
        )
        self.assertEqual(server.application, self.application)
        self.assertEqual(server.device, self.device)
        self.assertEqual(server.name, 'Web Server 1')
        self.assertEqual(server.role, ServerRoleChoices.WEB_SERVER)
        self.assertEqual(server.status, ServerStatusChoices.STATUS_ACTIVE)
        self.assertEqual(server.primary_ip4, self.ip_address)
        self.assertEqual(server.cpu_cores, 4)
        self.assertEqual(server.memory_gb, 8)
        self.assertEqual(server.storage_gb, 100)
        self.assertEqual(server.operating_system, 'Ubuntu 20.04')
        self.assertEqual(server.middleware, 'Apache, PHP')
        self.assertEqual(str(server), 'Web Server 1')

    def test_create_application_server_with_vm(self):
        """测试创建关联虚拟机的应用服务器"""
        server = ApplicationServer.objects.create(
            application=self.application,
            virtual_machine=self.virtual_machine,
            name='App Server 1',
            role=ServerRoleChoices.APPLICATION_SERVER,
            status=ServerStatusChoices.STATUS_ACTIVE
        )
        self.assertEqual(server.virtual_machine, self.virtual_machine)
        self.assertEqual(server.role, ServerRoleChoices.APPLICATION_SERVER)

    def test_unique_application_name(self):
        """测试应用系统内服务器名称唯一性"""
        ApplicationServer.objects.create(
            application=self.application,
            name='Server 1',
            role=ServerRoleChoices.WEB_SERVER
        )
        with self.assertRaises(Exception):
            ApplicationServer.objects.create(
                application=self.application,
                name='Server 1',
                role=ServerRoleChoices.APPLICATION_SERVER
            )

    def test_clean_validation(self):
        """测试clean方法的验证逻辑"""
        # 测试既没有设备也没有虚拟机的情况
        server = ApplicationServer(
            application=self.application,
            name='Invalid Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        with self.assertRaises(ValidationError):
            server.clean()
        
        # 测试同时有设备和虚拟机的情况
        server = ApplicationServer(
            application=self.application,
            device=self.device,
            virtual_machine=self.virtual_machine,
            name='Invalid Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        with self.assertRaises(ValidationError):
            server.clean()

    def test_primary_ip_property(self):
        """测试primary_ip属性"""
        server = ApplicationServer.objects.create(
            application=self.application,
            device=self.device,
            name='Test Server',
            role=ServerRoleChoices.WEB_SERVER,
            primary_ip4=self.ip_address
        )
        self.assertEqual(server.primary_ip, self.ip_address)

    def test_host_property(self):
        """测试host属性"""
        server = ApplicationServer.objects.create(
            application=self.application,
            device=self.device,
            name='Test Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        self.assertEqual(server.host, self.device)
        
        server_vm = ApplicationServer.objects.create(
            application=self.application,
            virtual_machine=self.virtual_machine,
            name='Test VM Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        self.assertEqual(server_vm.host, self.virtual_machine)

    def test_get_status_color(self):
        """测试获取状态颜色"""
        server = ApplicationServer.objects.create(
            application=self.application,
            device=self.device,
            name='Test Server',
            role=ServerRoleChoices.WEB_SERVER,
            status=ServerStatusChoices.STATUS_ACTIVE
        )
        color = server.get_status_color()
        self.assertIsNotNone(color)


class TestApplicationEndpoint(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(
            name='Test App',
            slug='test-app'
        )
        
        # 创建应用服务器
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
        
        cls.server = ApplicationServer.objects.create(
            application=cls.application,
            device=device,
            name='Web Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        
        cls.ip_address = IPAddress.objects.create(
            address='192.168.1.100/24'
        )

    def test_create_application_endpoint(self):
        """测试创建应用端点"""
        endpoint = ApplicationEndpoint.objects.create(
            application=self.application,
            server=self.server,
            name='Web UI',
            type=EndpointTypeChoices.WEB_UI,
            status=EndpointStatusChoices.STATUS_ACTIVE,
            url='https://example.com',
            ip_address=self.ip_address,
            port=443,
            protocol='HTTPS',
            path='/admin',
            is_public=True,
            is_load_balanced=False,
            health_check_url='https://example.com/health',
            authentication_required=True,
            ssl_enabled=True,
            documentation_url='https://docs.example.com',
            description='Main web interface'
        )
        self.assertEqual(endpoint.application, self.application)
        self.assertEqual(endpoint.server, self.server)
        self.assertEqual(endpoint.name, 'Web UI')
        self.assertEqual(endpoint.type, EndpointTypeChoices.WEB_UI)
        self.assertEqual(endpoint.status, EndpointStatusChoices.STATUS_ACTIVE)
        self.assertEqual(endpoint.url, 'https://example.com')
        self.assertEqual(endpoint.ip_address, self.ip_address)
        self.assertEqual(endpoint.port, 443)
        self.assertEqual(endpoint.protocol, 'HTTPS')
        self.assertEqual(endpoint.path, '/admin')
        self.assertTrue(endpoint.is_public)
        self.assertFalse(endpoint.is_load_balanced)
        self.assertEqual(endpoint.health_check_url, 'https://example.com/health')
        self.assertTrue(endpoint.authentication_required)
        self.assertTrue(endpoint.ssl_enabled)
        self.assertEqual(endpoint.documentation_url, 'https://docs.example.com')
        self.assertEqual(str(endpoint), 'Web UI')

    def test_unique_application_name(self):
        """测试应用系统内端点名称唯一性"""
        ApplicationEndpoint.objects.create(
            application=self.application,
            name='API Endpoint',
            type=EndpointTypeChoices.API
        )
        with self.assertRaises(Exception):
            ApplicationEndpoint.objects.create(
                application=self.application,
                name='API Endpoint',
                type=EndpointTypeChoices.WEB_UI
            )

    def test_clean_validation(self):
        """测试clean方法的验证逻辑"""
        # 测试无效的URL
        endpoint = ApplicationEndpoint(
            application=self.application,
            name='Invalid Endpoint',
            type=EndpointTypeChoices.WEB_UI,
            url='invalid-url'
        )
        with self.assertRaises(ValidationError):
            endpoint.clean()
        
        # 测试无效的健康检查URL
        endpoint = ApplicationEndpoint(
            application=self.application,
            name='Invalid Health Check',
            type=EndpointTypeChoices.API,
            health_check_url='invalid-url'
        )
        with self.assertRaises(ValidationError):
            endpoint.clean()

    def test_full_address_property(self):
        """测试full_address属性"""
        # 测试完整URL
        endpoint = ApplicationEndpoint.objects.create(
            application=self.application,
            name='Full URL Endpoint',
            type=EndpointTypeChoices.WEB_UI,
            url='https://example.com/app'
        )
        self.assertEqual(endpoint.full_address, 'https://example.com/app')
        
        # 测试IP+端口+路径组合
        endpoint2 = ApplicationEndpoint.objects.create(
            application=self.application,
            name='IP Endpoint',
            type=EndpointTypeChoices.API,
            ip_address=self.ip_address,
            port=8080,
            path='/api/v1'
        )
        expected = f'{self.ip_address.address.ip}:8080/api/v1'
        self.assertEqual(endpoint2.full_address, expected)
        
        # 测试只有IP地址
        endpoint3 = ApplicationEndpoint.objects.create(
            application=self.application,
            name='IP Only Endpoint',
            type=EndpointTypeChoices.SSH,
            ip_address=self.ip_address
        )
        self.assertEqual(endpoint3.full_address, str(self.ip_address.address.ip))

    def test_get_status_color(self):
        """测试获取状态颜色"""
        endpoint = ApplicationEndpoint.objects.create(
            application=self.application,
            name='Test Endpoint',
            type=EndpointTypeChoices.WEB_UI,
            status=EndpointStatusChoices.STATUS_ACTIVE
        )
        color = endpoint.get_status_color()
        self.assertIsNotNone(color)


class TestApplicationPersonnel(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(
            name='Test App',
            slug='test-app'
        )
        cls.contact = Contact.objects.create(
            name='John Doe',
            email='john.doe@example.com'
        )

    def test_create_application_personnel(self):
        """测试创建应用人员"""
        from datetime import date
        
        personnel = ApplicationPersonnel.objects.create(
            application=self.application,
            contact=self.contact,
            name='John Doe',
            role=PersonnelRoleChoices.OWNER,
            email='john.doe@example.com',
            phone='+1234567890',
            department='IT Department',
            title='Senior Developer',
            is_primary=True,
            is_emergency_contact=True,
            start_date=date(2023, 1, 1),
            end_date=date(2024, 12, 31),
            notes='Primary application owner',
            description='Responsible for overall application management'
        )
        self.assertEqual(personnel.application, self.application)
        self.assertEqual(personnel.contact, self.contact)
        self.assertEqual(personnel.name, 'John Doe')
        self.assertEqual(personnel.role, PersonnelRoleChoices.OWNER)
        self.assertEqual(personnel.email, 'john.doe@example.com')
        self.assertEqual(personnel.phone, '+1234567890')
        self.assertEqual(personnel.department, 'IT Department')
        self.assertEqual(personnel.title, 'Senior Developer')
        self.assertTrue(personnel.is_primary)
        self.assertTrue(personnel.is_emergency_contact)
        self.assertEqual(personnel.start_date, date(2023, 1, 1))
        self.assertEqual(personnel.end_date, date(2024, 12, 31))
        self.assertEqual(personnel.notes, 'Primary application owner')
        self.assertEqual(str(personnel), 'John Doe (Owner)')

    def test_unique_application_name_role(self):
        """测试应用系统内人员名称和角色的唯一性"""
        ApplicationPersonnel.objects.create(
            application=self.application,
            name='John Doe',
            role=PersonnelRoleChoices.OWNER
        )
        with self.assertRaises(Exception):
            ApplicationPersonnel.objects.create(
                application=self.application,
                name='John Doe',
                role=PersonnelRoleChoices.OWNER
            )

    def test_different_roles_allowed(self):
        """测试同一人员在同一应用系统中可以有不同角色"""
        ApplicationPersonnel.objects.create(
            application=self.application,
            name='John Doe',
            role=PersonnelRoleChoices.OWNER
        )
        personnel2 = ApplicationPersonnel.objects.create(
            application=self.application,
            name='John Doe',
            role=PersonnelRoleChoices.DEVELOPER
        )
        self.assertEqual(personnel2.name, 'John Doe')
        self.assertEqual(personnel2.role, PersonnelRoleChoices.DEVELOPER)

    def test_clean_validation(self):
        """测试clean方法的验证逻辑"""
        from datetime import date
        
        # 测试结束日期早于开始日期
        personnel = ApplicationPersonnel(
            application=self.application,
            name='Invalid Personnel',
            role=PersonnelRoleChoices.DEVELOPER,
            start_date=date(2024, 1, 1),
            end_date=date(2023, 12, 31)
        )
        with self.assertRaises(ValidationError):
            personnel.clean()

    def test_is_active_property(self):
        """测试is_active属性"""
        from datetime import date, timedelta
        
        today = date.today()
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)
        
        # 测试当前活跃的人员
        personnel_active = ApplicationPersonnel.objects.create(
            application=self.application,
            name='Active Personnel',
            role=PersonnelRoleChoices.DEVELOPER,
            start_date=yesterday,
            end_date=tomorrow
        )
        self.assertTrue(personnel_active.is_active)
        
        # 测试已结束的人员
        personnel_ended = ApplicationPersonnel.objects.create(
            application=self.application,
            name='Ended Personnel',
            role=PersonnelRoleChoices.TESTER,
            start_date=yesterday - timedelta(days=10),
            end_date=yesterday
        )
        self.assertFalse(personnel_ended.is_active)
        
        # 测试未开始的人员
        personnel_future = ApplicationPersonnel.objects.create(
            application=self.application,
            name='Future Personnel',
            role=PersonnelRoleChoices.OPERATOR,
            start_date=tomorrow,
            end_date=tomorrow + timedelta(days=30)
        )
        self.assertFalse(personnel_future.is_active)
        
        # 测试没有日期限制的人员
        personnel_no_dates = ApplicationPersonnel.objects.create(
            application=self.application,
            name='No Dates Personnel',
            role=PersonnelRoleChoices.ADMINISTRATOR
        )
        self.assertTrue(personnel_no_dates.is_active)

    def test_contact_info_property(self):
        """测试contact_info属性"""
        personnel = ApplicationPersonnel.objects.create(
            application=self.application,
            name='Test Personnel',
            role=PersonnelRoleChoices.DEVELOPER,
            email='test@example.com',
            phone='+1234567890'
        )
        contact_info = personnel.contact_info
        self.assertIn('test@example.com', contact_info)
        self.assertIn('+1234567890', contact_info)
        
        # 测试没有联系信息的情况
        personnel_no_contact = ApplicationPersonnel.objects.create(
            application=self.application,
            name='No Contact Personnel',
            role=PersonnelRoleChoices.SUPPORT
        )
        self.assertIsNone(personnel_no_contact.contact_info)