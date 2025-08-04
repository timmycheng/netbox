from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant, Contact
from virtualization.models import VirtualMachine, Cluster, ClusterType
from appm.choices import *
from appm.forms import *
from appm.models import *


class ApplicationGroupFormTest(TestCase):

    def test_valid_form(self):
        """测试有效的应用系统分组表单"""
        form_data = {
            'name': 'Web Applications',
            'slug': 'web-applications',
            'description': 'Web application group'
        }
        form = ApplicationGroupForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """测试必填字段"""
        form = ApplicationGroupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('slug', form.errors)

    def test_unique_name_validation(self):
        """测试名称唯一性验证"""
        ApplicationGroup.objects.create(
            name='Existing Group',
            slug='existing-group'
        )
        form_data = {
            'name': 'Existing Group',
            'slug': 'new-slug'
        }
        form = ApplicationGroupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_unique_slug_validation(self):
        """测试slug唯一性验证"""
        ApplicationGroup.objects.create(
            name='Existing Group',
            slug='existing-slug'
        )
        form_data = {
            'name': 'New Group',
            'slug': 'existing-slug'
        }
        form = ApplicationGroupForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('slug', form.errors)


class ApplicationFormTest(TestCase):

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

    def test_valid_form(self):
        """测试有效的应用系统表单"""
        form_data = {
            'name': 'Test Application',
            'slug': 'test-application',
            'group': self.group.pk,
            'status': ApplicationStatusChoices.STATUS_ACTIVE,
            'tenant': self.tenant.pk,
            'environment': ApplicationEnvironmentChoices.PRODUCTION,
            'criticality': ApplicationCriticalityChoices.HIGH,
            'version': '1.0.0',
            'owner': 'John Doe',
            'business_unit': 'IT Department',
            'description': 'Test application description'
        }
        form = ApplicationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """测试必填字段"""
        form = ApplicationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('slug', form.errors)

    def test_unique_name_environment_validation(self):
        """测试名称和环境的唯一性验证"""
        Application.objects.create(
            name='Existing App',
            slug='existing-app',
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        form_data = {
            'name': 'Existing App',
            'slug': 'new-slug',
            'environment': ApplicationEnvironmentChoices.PRODUCTION
        }
        form = ApplicationForm(data=form_data)
        self.assertFalse(form.is_valid())
        # The unique constraint error might be in __all__ or specific fields
        self.assertTrue(form.errors)

    def test_different_environments_allowed(self):
        """测试相同名称在不同环境下允许创建"""
        Application.objects.create(
            name='Test App',
            slug='test-app-prod',
            environment=ApplicationEnvironmentChoices.PRODUCTION
        )
        form_data = {
            'name': 'Test App',
            'slug': 'test-app-staging',
            'environment': ApplicationEnvironmentChoices.STAGING
        }
        form = ApplicationForm(data=form_data)
        self.assertTrue(form.is_valid())


class ApplicationServerFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.application = Application.objects.create(
            name='Test App',
            slug='test-app'
        )
        
        # 创建设备相关对象
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
        cls.device = Device.objects.create(
            name='test-device',
            device_type=device_type,
            role=device_role,
            site=site
        )
        
        # 创建虚拟机相关对象
        cluster_type = ClusterType.objects.create(
            name='Test Cluster Type',
            slug='test-cluster-type'
        )
        cluster = Cluster.objects.create(
            name='Test Cluster',
            type=cluster_type
        )
        cls.virtual_machine = VirtualMachine.objects.create(
            name='test-vm',
            cluster=cluster
        )
        
        cls.ip_address = IPAddress.objects.create(
            address='192.168.1.100/24'
        )

    def test_valid_form_with_device(self):
        """测试有效的应用服务器表单（关联设备）"""
        form_data = {
            'application': self.application.pk,
            'device': self.device.pk,
            'name': 'Web Server 1',
            'role': ServerRoleChoices.WEB_SERVER,
            'status': ServerStatusChoices.STATUS_ACTIVE,
            'primary_ip4': self.ip_address.pk,
            'cpu_cores': 4,
            'memory_gb': 8,
            'storage_gb': 100,
            'operating_system': 'Ubuntu 20.04',
            'middleware': 'Apache, PHP',
            'description': 'Primary web server'
        }
        form = ApplicationServerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_vm(self):
        """测试有效的应用服务器表单（关联虚拟机）"""
        form_data = {
            'application': self.application.pk,
            'virtual_machine': self.virtual_machine.pk,
            'name': 'App Server 1',
            'role': ServerRoleChoices.APPLICATION_SERVER,
            'status': ServerStatusChoices.STATUS_ACTIVE,
            'description': 'Application server'
        }
        form = ApplicationServerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """测试必填字段"""
        form = ApplicationServerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('application', form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('role', form.errors)

    def test_unique_application_name_validation(self):
        """测试应用系统内名称唯一性验证"""
        ApplicationServer.objects.create(
            application=self.application,
            device=self.device,
            name='Existing Server',
            role=ServerRoleChoices.WEB_SERVER
        )
        form_data = {
            'application': self.application.pk,
            'name': 'Existing Server',
            'role': ServerRoleChoices.APPLICATION_SERVER
        }
        form = ApplicationServerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)


class ApplicationEndpointFormTest(TestCase):

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

    def test_valid_form_with_url(self):
        """测试有效的应用端点表单（使用URL）"""
        form_data = {
            'application': self.application.pk,
            'server': self.server.pk,
            'name': 'Web UI',
            'type': EndpointTypeChoices.WEB_UI,
            'status': EndpointStatusChoices.STATUS_ACTIVE,
            'url': 'https://example.com',
            'is_public': True,
            'ssl_enabled': True,
            'authentication_required': True,
            'description': 'Main web interface'
        }
        form = ApplicationEndpointForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_valid_form_with_ip_port(self):
        """测试有效的应用端点表单（使用IP和端口）"""
        form_data = {
            'application': self.application.pk,
            'server': self.server.pk,
            'name': 'API Endpoint',
            'type': EndpointTypeChoices.API,
            'status': EndpointStatusChoices.STATUS_ACTIVE,
            'ip_address': self.ip_address.pk,
            'port': 8080,
            'protocol': 'HTTP',
            'path': '/api/v1',
            'description': 'REST API endpoint'
        }
        form = ApplicationEndpointForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """测试必填字段"""
        form = ApplicationEndpointForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('application', form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('type', form.errors)

    def test_unique_application_name_validation(self):
        """测试应用系统内名称唯一性验证"""
        ApplicationEndpoint.objects.create(
            application=self.application,
            name='Existing Endpoint',
            type=EndpointTypeChoices.WEB_UI
        )
        form_data = {
            'application': self.application.pk,
            'name': 'Existing Endpoint',
            'type': EndpointTypeChoices.API
        }
        form = ApplicationEndpointForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_invalid_url_validation(self):
        """测试无效URL验证"""
        form_data = {
            'application': self.application.pk,
            'name': 'Invalid URL Endpoint',
            'type': EndpointTypeChoices.WEB_UI,
            'url': 'invalid-url'
        }
        form = ApplicationEndpointForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('url', form.errors)

    def test_invalid_health_check_url_validation(self):
        """测试无效健康检查URL验证"""
        form_data = {
            'application': self.application.pk,
            'name': 'Invalid Health Check',
            'type': EndpointTypeChoices.API,
            'health_check_url': 'invalid-url'
        }
        form = ApplicationEndpointForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('health_check_url', form.errors)


class ApplicationPersonnelFormTest(TestCase):

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

    def test_valid_form(self):
        """测试有效的应用人员表单"""
        form_data = {
            'application': self.application.pk,
            'contact': self.contact.pk,
            'name': 'John Doe',
            'role': PersonnelRoleChoices.OWNER,
            'email': 'john.doe@example.com',
            'phone': '+1234567890',
            'department': 'IT Department',
            'title': 'Senior Developer',
            'is_primary': True,
            'is_emergency_contact': True,
            'start_date': '2023-01-01',
            'end_date': '2024-12-31',
            'notes': 'Primary application owner',
            'description': 'Responsible for overall application management'
        }
        form = ApplicationPersonnelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        """测试必填字段"""
        form = ApplicationPersonnelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('application', form.errors)
        self.assertIn('name', form.errors)
        self.assertIn('role', form.errors)

    def test_unique_application_name_role_validation(self):
        """测试应用系统内名称和角色唯一性验证"""
        ApplicationPersonnel.objects.create(
            application=self.application,
            name='John Doe',
            role=PersonnelRoleChoices.OWNER
        )
        form_data = {
            'application': self.application.pk,
            'name': 'John Doe',
            'role': PersonnelRoleChoices.OWNER
        }
        form = ApplicationPersonnelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors)

    def test_different_roles_allowed(self):
        """测试同一人员在同一应用系统中可以有不同角色"""
        ApplicationPersonnel.objects.create(
            application=self.application,
            name='John Doe',
            role=PersonnelRoleChoices.OWNER
        )
        form_data = {
            'application': self.application.pk,
            'name': 'John Doe',
            'role': PersonnelRoleChoices.DEVELOPER
        }
        form = ApplicationPersonnelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email_validation(self):
        """测试无效邮箱验证"""
        form_data = {
            'application': self.application.pk,
            'name': 'Test Person',
            'role': PersonnelRoleChoices.DEVELOPER,
            'email': 'invalid-email'
        }
        form = ApplicationPersonnelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_date_validation(self):
        """测试日期验证（结束日期不能早于开始日期）"""
        form_data = {
            'application': self.application.pk,
            'name': 'Test Person',
            'role': PersonnelRoleChoices.DEVELOPER,
            'start_date': '2024-01-01',
            'end_date': '2023-12-31'
        }
        form = ApplicationPersonnelForm(data=form_data)
        self.assertFalse(form.is_valid())
        # The validation error might be in clean() method
        self.assertTrue(form.errors)