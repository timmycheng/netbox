from django.urls import reverse
from rest_framework import status

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant, Contact
from virtualization.models import VirtualMachine, Cluster, ClusterType
from appm.choices import *
from appm.models import *
from utilities.testing import APITestCase, APIViewTestCases


class AppTest(APITestCase):

    def test_root(self):
        url = reverse('appm-api:api-root')
        response = self.client.get('{}?format=api'.format(url), **self.header)
        self.assertEqual(response.status_code, 200)


class ApplicationGroupTest(APIViewTestCases.APIViewTestCase):
    model = ApplicationGroup
    brief_fields = ['description', 'display', 'id', 'name', 'slug', 'url']
    create_data = [
        {
            'name': 'Web Applications',
            'slug': 'web-applications',
        },
        {
            'name': 'Database Applications',
            'slug': 'database-applications',
        },
        {
            'name': 'API Services',
            'slug': 'api-services',
        },
    ]
    bulk_update_data = {
        'description': 'Updated description',
    }

    @classmethod
    def setUpTestData(cls):
        application_groups = (
            ApplicationGroup(name='Group 1', slug='group-1'),
            ApplicationGroup(name='Group 2', slug='group-2'),
            ApplicationGroup(name='Group 3', slug='group-3'),
        )
        ApplicationGroup.objects.bulk_create(application_groups)


class ApplicationTest(APIViewTestCases.APIViewTestCase):
    model = Application
    brief_fields = ['description', 'display', 'id', 'name', 'slug', 'url']
    bulk_update_data = {
        'description': 'Updated description',
    }

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
                name='App 1',
                slug='app-1',
                group=application_groups[0],
                tenant=tenants[0],
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='App 2',
                slug='app-2',
                group=application_groups[0],
                tenant=tenants[0],
                environment=ApplicationEnvironmentChoices.STAGING
            ),
            Application(
                name='App 3',
                slug='app-3',
                group=application_groups[1],
                tenant=tenants[1],
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
        )
        Application.objects.bulk_create(applications)

        cls.create_data = [
            {
                'name': 'New App 1',
                'slug': 'new-app-1',
                'group': application_groups[0].pk,
                'environment': ApplicationEnvironmentChoices.DEVELOPMENT,
                'status': ApplicationStatusChoices.STATUS_ACTIVE,
                'criticality': ApplicationCriticalityChoices.MEDIUM,
            },
            {
                'name': 'New App 2',
                'slug': 'new-app-2',
                'group': application_groups[1].pk,
                'environment': ApplicationEnvironmentChoices.TESTING,
                'status': ApplicationStatusChoices.STATUS_PLANNED,
                'criticality': ApplicationCriticalityChoices.HIGH,
            },
            {
                'name': 'New App 3',
                'slug': 'new-app-3',
                'environment': ApplicationEnvironmentChoices.PRODUCTION,
                'status': ApplicationStatusChoices.STATUS_ACTIVE,
                'criticality': ApplicationCriticalityChoices.LOW,
            },
        ]


class ApplicationServerTest(APIViewTestCases.APIViewTestCase):
    model = ApplicationServer
    brief_fields = ['description', 'display', 'id', 'name', 'url']
    bulk_update_data = {
        'description': 'Updated description',
    }

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统
        application_group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        applications = (
            Application(
                name='App 1',
                slug='app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='App 2',
                slug='app-2',
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
            Device(
                name='test-device-3',
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
        virtual_machines = (
            VirtualMachine(
                name='test-vm-1',
                cluster=cluster
            ),
            VirtualMachine(
                name='test-vm-2',
                cluster=cluster
            ),
        )
        VirtualMachine.objects.bulk_create(virtual_machines)

        # 创建应用服务器
        application_servers = (
            ApplicationServer(
                application=applications[0],
                device=devices[0],
                name='Server 1',
                role=ServerRoleChoices.WEB_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE
            ),
            ApplicationServer(
                application=applications[0],
                virtual_machine=virtual_machines[0],
                name='Server 2',
                role=ServerRoleChoices.APPLICATION_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE
            ),
            ApplicationServer(
                application=applications[1],
                device=devices[1],
                name='Server 3',
                role=ServerRoleChoices.DATABASE_SERVER,
                status=ServerStatusChoices.STATUS_PLANNED
            ),
        )
        ApplicationServer.objects.bulk_create(application_servers)

        cls.create_data = [
            {
                'application': applications[0].pk,
                'device': devices[2].pk,
                'name': 'New Server 1',
                'role': ServerRoleChoices.CACHE_SERVER,
                'status': ServerStatusChoices.STATUS_ACTIVE,
            },
            {
                'application': applications[1].pk,
                'virtual_machine': virtual_machines[1].pk,
                'name': 'New Server 2',
                'role': ServerRoleChoices.LOAD_BALANCER,
                'status': ServerStatusChoices.STATUS_PLANNED,
            },
            {
                'application': applications[0].pk,
                'device': devices[1],  # This will be converted to pk in the test
                'name': 'New Server 3',
                'role': ServerRoleChoices.FILE_SERVER,
                'status': ServerStatusChoices.STATUS_ACTIVE,
            },
        ]
        
        # Convert device object to pk for API test
        cls.create_data[2]['device'] = devices[1].pk


class ApplicationEndpointTest(APIViewTestCases.APIViewTestCase):
    model = ApplicationEndpoint
    brief_fields = ['description', 'display', 'id', 'name', 'url']
    bulk_update_data = {
        'description': 'Updated description',
    }

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统和服务器
        application_group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        applications = (
            Application(
                name='App 1',
                slug='app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='App 2',
                slug='app-2',
                group=application_group,
                environment=ApplicationEnvironmentChoices.STAGING
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
                name='Server 1',
                role=ServerRoleChoices.WEB_SERVER
            ),
            ApplicationServer(
                application=applications[1],
                device=device,
                name='Server 2',
                role=ServerRoleChoices.APPLICATION_SERVER
            ),
        )
        ApplicationServer.objects.bulk_create(servers)

        # 创建IP地址
        ip_addresses = (
            IPAddress(address='192.168.1.100/24'),
            IPAddress(address='192.168.1.101/24'),
        )
        IPAddress.objects.bulk_create(ip_addresses)

        # 创建应用端点
        application_endpoints = (
            ApplicationEndpoint(
                application=applications[0],
                server=servers[0],
                name='Endpoint 1',
                type=EndpointTypeChoices.WEB_UI,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                url='https://app1.example.com'
            ),
            ApplicationEndpoint(
                application=applications[0],
                server=servers[0],
                name='Endpoint 2',
                type=EndpointTypeChoices.API,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                ip_address=ip_addresses[0],
                port=8080
            ),
            ApplicationEndpoint(
                application=applications[1],
                server=servers[1],
                name='Endpoint 3',
                type=EndpointTypeChoices.DATABASE,
                status=EndpointStatusChoices.STATUS_PLANNED,
                ip_address=ip_addresses[1],
                port=5432
            ),
        )
        ApplicationEndpoint.objects.bulk_create(application_endpoints)

        cls.create_data = [
            {
                'application': applications[0].pk,
                'server': servers[0].pk,
                'name': 'New Endpoint 1',
                'type': EndpointTypeChoices.WEB_SERVICE,
                'status': EndpointStatusChoices.STATUS_ACTIVE,
                'url': 'https://service.example.com',
            },
            {
                'application': applications[1].pk,
                'server': servers[1].pk,
                'name': 'New Endpoint 2',
                'type': EndpointTypeChoices.FTP,
                'status': EndpointStatusChoices.STATUS_PLANNED,
                'ip_address': ip_addresses[0].pk,
                'port': 21,
            },
            {
                'application': applications[0].pk,
                'name': 'New Endpoint 3',
                'type': EndpointTypeChoices.SSH,
                'status': EndpointStatusChoices.STATUS_ACTIVE,
                'ip_address': ip_addresses[1].pk,
                'port': 22,
            },
        ]


class ApplicationPersonnelTest(APIViewTestCases.APIViewTestCase):
    model = ApplicationPersonnel
    brief_fields = ['description', 'display', 'id', 'name', 'url']
    bulk_update_data = {
        'description': 'Updated description',
    }

    @classmethod
    def setUpTestData(cls):
        # 创建应用系统
        application_group = ApplicationGroup.objects.create(
            name='Web Applications',
            slug='web-applications'
        )
        applications = (
            Application(
                name='App 1',
                slug='app-1',
                group=application_group,
                environment=ApplicationEnvironmentChoices.PRODUCTION
            ),
            Application(
                name='App 2',
                slug='app-2',
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
                start_date=date(2023, 1, 1)
            ),
            ApplicationPersonnel(
                application=applications[0],
                contact=contacts[1],
                name='Jane Smith',
                role=PersonnelRoleChoices.DEVELOPER,
                email='jane.smith@example.com',
                start_date=date(2023, 6, 1)
            ),
            ApplicationPersonnel(
                application=applications[1],
                contact=contacts[0],
                name='John Doe',
                role=PersonnelRoleChoices.ADMINISTRATOR,
                email='john.doe@example.com',
                start_date=date(2023, 3, 1)
            ),
        )
        ApplicationPersonnel.objects.bulk_create(application_personnel)

        cls.create_data = [
            {
                'application': applications[0].pk,
                'contact': contacts[0].pk,
                'name': 'Bob Wilson',
                'role': PersonnelRoleChoices.TESTER,
                'email': 'bob.wilson@example.com',
            },
            {
                'application': applications[1].pk,
                'contact': contacts[1].pk,
                'name': 'Alice Brown',
                'role': PersonnelRoleChoices.OPERATOR,
                'email': 'alice.brown@example.com',
            },
            {
                'application': applications[0].pk,
                'name': 'Charlie Davis',
                'role': PersonnelRoleChoices.SUPPORT,
                'email': 'charlie.davis@example.com',
            },
        ]