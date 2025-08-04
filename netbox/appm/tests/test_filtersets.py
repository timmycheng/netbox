from django.test import TestCase

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant, Contact
from virtualization.models import VirtualMachine, Cluster, ClusterType
from appm.choices import *
from appm.filtersets import *
from appm.models import *
from utilities.testing import ChangeLoggedFilterSetTests


class ApplicationGroupFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationGroup.objects.all()
    filterset = ApplicationGroupFilterSet

    @classmethod
    def setUpTestData(cls):
        application_groups = (
            ApplicationGroup(name='Web Applications', slug='web-applications', description='Web apps'),
            ApplicationGroup(name='Database Applications', slug='database-applications', description='DB apps'),
            ApplicationGroup(name='API Services', slug='api-services', description='API services'),
        )
        ApplicationGroup.objects.bulk_create(application_groups)

    def test_name(self):
        """测试按名称过滤"""
        params = {'name': ['Web Applications', 'API Services']}
        filterset = ApplicationGroupFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        self.assertIn('Web Applications', [obj.name for obj in filterset.qs])
        self.assertIn('API Services', [obj.name for obj in filterset.qs])

    def test_slug(self):
        """测试按slug过滤"""
        params = {'slug': ['web-applications']}
        filterset = ApplicationGroupFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().slug, 'web-applications')

    def test_description(self):
        """测试按描述过滤"""
        params = {'description': ['Web apps']}
        filterset = ApplicationGroupFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().description, 'Web apps')


class ApplicationFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = Application.objects.all()
    filterset = ApplicationFilterSet

    @classmethod
    def setUpTestData(cls):
        application_groups = (
            ApplicationGroup(name='Web Applications', slug='web-applications'),
            ApplicationGroup(name='Database Applications', slug='database-applications'),
        )
        ApplicationGroup.objects.bulk_create(application_groups)

        tenants = (
            Tenant(name='Tenant A', slug='tenant-a'),
            Tenant(name='Tenant B', slug='tenant-b'),
        )
        Tenant.objects.bulk_create(tenants)

        applications = (
            Application(
                name='Web App 1',
                slug='web-app-1',
                group=application_groups[0],
                tenant=tenants[0],
                status=ApplicationStatusChoices.STATUS_ACTIVE,
                environment=ApplicationEnvironmentChoices.PRODUCTION,
                criticality=ApplicationCriticalityChoices.HIGH,
                owner='John Doe',
                business_unit='IT Department'
            ),
            Application(
                name='Web App 2',
                slug='web-app-2',
                group=application_groups[0],
                tenant=tenants[0],
                status=ApplicationStatusChoices.STATUS_PLANNED,
                environment=ApplicationEnvironmentChoices.STAGING,
                criticality=ApplicationCriticalityChoices.MEDIUM,
                owner='Jane Smith',
                business_unit='Engineering'
            ),
            Application(
                name='DB App 1',
                slug='db-app-1',
                group=application_groups[1],
                tenant=tenants[1],
                status=ApplicationStatusChoices.STATUS_ACTIVE,
                environment=ApplicationEnvironmentChoices.PRODUCTION,
                criticality=ApplicationCriticalityChoices.CRITICAL,
                owner='Bob Wilson',
                business_unit='Data Team'
            ),
        )
        Application.objects.bulk_create(applications)

    def test_name(self):
        """测试按名称过滤"""
        params = {'name': ['Web App 1', 'DB App 1']}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)

    def test_slug(self):
        """测试按slug过滤"""
        params = {'slug': ['web-app-1']}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().slug, 'web-app-1')

    def test_group(self):
        """测试按应用分组过滤"""
        group = ApplicationGroup.objects.get(slug='web-applications')
        params = {'group_id': [group.pk]}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for app in filterset.qs:
            self.assertEqual(app.group, group)

    def test_tenant(self):
        """测试按租户过滤"""
        tenant = Tenant.objects.get(slug='tenant-a')
        params = {'tenant_id': [tenant.pk]}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for app in filterset.qs:
            self.assertEqual(app.tenant, tenant)

    def test_status(self):
        """测试按状态过滤"""
        params = {'status': [ApplicationStatusChoices.STATUS_ACTIVE]}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for app in filterset.qs:
            self.assertEqual(app.status, ApplicationStatusChoices.STATUS_ACTIVE)

    def test_environment(self):
        """测试按环境过滤"""
        params = {'environment': [ApplicationEnvironmentChoices.PRODUCTION]}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for app in filterset.qs:
            self.assertEqual(app.environment, ApplicationEnvironmentChoices.PRODUCTION)

    def test_criticality(self):
        """测试按重要性过滤"""
        params = {'criticality': [ApplicationCriticalityChoices.HIGH]}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().criticality, ApplicationCriticalityChoices.HIGH)

    def test_owner(self):
        """测试按负责人过滤"""
        params = {'owner': ['John Doe']}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().owner, 'John Doe')

    def test_business_unit(self):
        """测试按业务单元过滤"""
        params = {'business_unit': ['IT Department']}
        filterset = ApplicationFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().business_unit, 'IT Department')


class ApplicationServerFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationServer.objects.all()
    filterset = ApplicationServerFilterSet

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统
        application_group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        applications = (
            Application(
                name='Web App 1',
                slug='web-app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='Web App 2',
                slug='web-app-2',
                group=application_group,
                environment=ApplicationEnvironmentChoices.STAGING
            ),
        )
        Application.objects.bulk_create(applications)

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
        devices = (
            Device(
                name='test-device-1',
                device_type=device_type,
                role=device_role,
                site=site
            ),
            Device(
                name='test-device-2',
                device_type=device_type,
                role=device_role,
                site=site
            ),
        )
        Device.objects.bulk_create(devices)

        # 创建虚拟机相关对象
        cluster_type = ClusterType.objects.create(
            name='Test Cluster Type',
            slug='test-cluster-type'
        )
        cluster = Cluster.objects.create(
            name='Test Cluster',
            type=cluster_type
        )
        virtual_machine = VirtualMachine.objects.create(
            name='test-vm-1',
            cluster=cluster
        )

        # 创建应用服务器
        application_servers = (
            ApplicationServer(
                application=applications[0],
                device=devices[0],
                name='Web Server 1',
                role=ServerRoleChoices.WEB_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE,
                operating_system='Ubuntu 20.04'
            ),
            ApplicationServer(
                application=applications[0],
                virtual_machine=virtual_machine,
                name='App Server 1',
                role=ServerRoleChoices.APPLICATION_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE,
                operating_system='CentOS 8'
            ),
            ApplicationServer(
                application=applications[1],
                device=devices[1],
                name='DB Server 1',
                role=ServerRoleChoices.DATABASE_SERVER,
                status=ServerStatusChoices.STATUS_PLANNED,
                operating_system='Ubuntu 22.04'
            ),
        )
        ApplicationServer.objects.bulk_create(application_servers)

    def test_name(self):
        """测试按名称过滤"""
        params = {'name': ['Web Server 1', 'DB Server 1']}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)

    def test_application(self):
        """测试按应用系统过滤"""
        application = Application.objects.get(slug='web-app-1')
        params = {'application_id': [application.pk]}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for server in filterset.qs:
            self.assertEqual(server.application, application)

    def test_role(self):
        """测试按角色过滤"""
        params = {'role': [ServerRoleChoices.WEB_SERVER]}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().role, ServerRoleChoices.WEB_SERVER)

    def test_status(self):
        """测试按状态过滤"""
        params = {'status': [ServerStatusChoices.STATUS_ACTIVE]}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for server in filterset.qs:
            self.assertEqual(server.status, ServerStatusChoices.STATUS_ACTIVE)

    def test_device(self):
        """测试按设备过滤"""
        device = Device.objects.get(name='test-device-1')
        params = {'device_id': [device.pk]}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().device, device)

    def test_virtual_machine(self):
        """测试按虚拟机过滤"""
        vm = VirtualMachine.objects.get(name='test-vm-1')
        params = {'virtual_machine_id': [vm.pk]}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().virtual_machine, vm)

    def test_operating_system(self):
        """测试按操作系统过滤"""
        params = {'operating_system': ['Ubuntu 20.04']}
        filterset = ApplicationServerFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().operating_system, 'Ubuntu 20.04')


class ApplicationEndpointFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationEndpoint.objects.all()
    filterset = ApplicationEndpointFilterSet

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统和服务器
        application_group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        applications = (
            Application(
                name='Web App 1',
                slug='web-app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='API App 1',
                slug='api-app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
        )
        Application.objects.bulk_create(applications)

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

        servers = (
            ApplicationServer(
                application=applications[0],
                device=device,
                name='Web Server 1',
                role=ServerRoleChoices.WEB_SERVER
            ),
            ApplicationServer(
                application=applications[1],
                device=device,
                name='API Server 1',
                role=ServerRoleChoices.APPLICATION_SERVER
            ),
        )
        ApplicationServer.objects.bulk_create(servers)

        # 创建IP地址
        ip_address = IPAddress.objects.create(
            address='192.168.1.100/24'
        )

        # 创建应用端点
        application_endpoints = (
            ApplicationEndpoint(
                application=applications[0],
                server=servers[0],
                name='Web UI',
                type=EndpointTypeChoices.WEB_UI,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                url='https://webapp1.example.com',
                is_public=True,
                ssl_enabled=True,
                protocol='HTTPS'
            ),
            ApplicationEndpoint(
                application=applications[0],
                server=servers[0],
                name='Admin Panel',
                type=EndpointTypeChoices.WEB_UI,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                ip_address=ip_address,
                port=8080,
                protocol='HTTP'
            ),
            ApplicationEndpoint(
                application=applications[1],
                server=servers[1],
                name='REST API',
                type=EndpointTypeChoices.API,
                status=EndpointStatusChoices.STATUS_PLANNED,
                url='https://api.example.com/v1',
                is_public=True,
                protocol='HTTPS'
            ),
        )
        ApplicationEndpoint.objects.bulk_create(application_endpoints)

    def test_name(self):
        """测试按名称过滤"""
        params = {'name': ['Web UI', 'REST API']}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)

    def test_application(self):
        """测试按应用系统过滤"""
        application = Application.objects.get(slug='web-app-1')
        params = {'application_id': [application.pk]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertEqual(endpoint.application, application)

    def test_server(self):
        """测试按服务器过滤"""
        server = ApplicationServer.objects.get(name='Web Server 1')
        params = {'server_id': [server.pk]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertEqual(endpoint.server, server)

    def test_type(self):
        """测试按类型过滤"""
        params = {'type': [EndpointTypeChoices.WEB_UI]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertEqual(endpoint.type, EndpointTypeChoices.WEB_UI)

    def test_status(self):
        """测试按状态过滤"""
        params = {'status': [EndpointStatusChoices.STATUS_ACTIVE]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertEqual(endpoint.status, EndpointStatusChoices.STATUS_ACTIVE)

    def test_is_public(self):
        """测试按是否公网访问过滤"""
        params = {'is_public': [True]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertTrue(endpoint.is_public)

    def test_ssl_enabled(self):
        """测试按是否启用SSL过滤"""
        params = {'ssl_enabled': [True]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertTrue(endpoint.ssl_enabled)

    def test_protocol(self):
        """测试按协议过滤"""
        params = {'protocol': ['HTTPS']}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for endpoint in filterset.qs:
            self.assertEqual(endpoint.protocol, 'HTTPS')

    def test_port(self):
        """测试按端口过滤"""
        params = {'port': [8080]}
        filterset = ApplicationEndpointFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().port, 8080)


class ApplicationPersonnelFilterSetTest(TestCase, ChangeLoggedFilterSetTests):
    queryset = ApplicationPersonnel.objects.all()
    filterset = ApplicationPersonnelFilterSet

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统
        application_group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        applications = (
            Application(
                name='Web App 1',
                slug='web-app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='Web App 2',
                slug='web-app-2',
                group=application_group,
                environment=ApplicationEnvironmentChoices.STAGING
            ),
        )
        Application.objects.bulk_create(applications)

        # 创建联系人
        contacts = (
            Contact(name='John Doe', email='john.doe@example.com'),
            Contact(name='Jane Smith', email='jane.smith@example.com'),
        )
        Contact.objects.bulk_create(contacts)

        # 创建应用人员
        from datetime import date
        application_personnel = (
            ApplicationPersonnel(
                application=applications[0],
                contact=contacts[0],
                name='John Doe',
                role=PersonnelRoleChoices.OWNER,
                email='john.doe@example.com',
                phone='+1234567890',
                department='IT Department',
                title='Senior Developer',
                is_primary=True,
                start_date=date(2023, 1, 1)
            ),
            ApplicationPersonnel(
                application=applications[0],
                contact=contacts[1],
                name='Jane Smith',
                role=PersonnelRoleChoices.DEVELOPER,
                email='jane.smith@example.com',
                phone='+0987654321',
                department='Engineering',
                title='Software Engineer',
                is_emergency_contact=True,
                start_date=date(2023, 6, 1)
            ),
            ApplicationPersonnel(
                application=applications[1],
                contact=contacts[0],
                name='John Doe',
                role=PersonnelRoleChoices.ADMINISTRATOR,
                email='john.doe@example.com',
                department='IT Department',
                title='System Administrator',
                start_date=date(2023, 3, 1)
            ),
        )
        ApplicationPersonnel.objects.bulk_create(application_personnel)

    def test_name(self):
        """测试按名称过滤"""
        params = {'name': ['John Doe']}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for personnel in filterset.qs:
            self.assertEqual(personnel.name, 'John Doe')

    def test_application(self):
        """测试按应用系统过滤"""
        application = Application.objects.get(slug='web-app-1')
        params = {'application_id': [application.pk]}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for personnel in filterset.qs:
            self.assertEqual(personnel.application, application)

    def test_contact(self):
        """测试按联系人过滤"""
        contact = Contact.objects.get(name='John Doe')
        params = {'contact_id': [contact.pk]}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for personnel in filterset.qs:
            self.assertEqual(personnel.contact, contact)

    def test_role(self):
        """测试按角色过滤"""
        params = {'role': [PersonnelRoleChoices.OWNER]}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().role, PersonnelRoleChoices.OWNER)

    def test_department(self):
        """测试按部门过滤"""
        params = {'department': ['IT Department']}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 2)
        for personnel in filterset.qs:
            self.assertEqual(personnel.department, 'IT Department')

    def test_title(self):
        """测试按职位过滤"""
        params = {'title': ['Senior Developer']}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertEqual(filterset.qs.first().title, 'Senior Developer')

    def test_is_primary(self):
        """测试按是否主要负责人过滤"""
        params = {'is_primary': [True]}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertTrue(filterset.qs.first().is_primary)

    def test_is_emergency_contact(self):
        """测试按是否紧急联系人过滤"""
        params = {'is_emergency_contact': [True]}
        filterset = ApplicationPersonnelFilterSet(params, self.queryset)
        self.assertEqual(filterset.qs.count(), 1)
        self.assertTrue(filterset.qs.first().is_emergency_contact)