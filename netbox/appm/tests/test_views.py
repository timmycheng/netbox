from django.test import override_settings
from django.urls import reverse

from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site
from ipam.models import IPAddress
from tenancy.models import Tenant, Contact
from virtualization.models import VirtualMachine, Cluster, ClusterType
from appm.choices import *
from appm.models import *
from utilities.testing import ViewTestCases, create_tags


class ApplicationGroupTestCase(ViewTestCases.OrganizationalObjectViewTestCase):
    model = ApplicationGroup

    @classmethod
    def setUpTestData(cls):
        application_groups = (
            ApplicationGroup(name='Web Applications', slug='web-applications'),
            ApplicationGroup(name='Database Applications', slug='database-applications'),
            ApplicationGroup(name='API Services', slug='api-services'),
        )
        ApplicationGroup.objects.bulk_create(application_groups)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'Mobile Applications',
            'slug': 'mobile-applications',
            'description': 'Mobile application group',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug,description",
            "Desktop Applications,desktop-applications,Desktop application group",
            "Cloud Services,cloud-services,Cloud service group",
            "Legacy Systems,legacy-systems,Legacy system group",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{application_groups[0].pk},Web Applications,Updated web applications",
            f"{application_groups[1].pk},Database Applications,Updated database applications",
            f"{application_groups[2].pk},API Services,Updated API services",
        )

        cls.bulk_edit_data = {
            'description': 'Bulk updated description',
        }


class ApplicationTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = Application

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
                criticality=ApplicationCriticalityChoices.HIGH
            ),
            Application(
                name='Web App 2',
                slug='web-app-2',
                group=application_groups[0],
                tenant=tenants[0],
                status=ApplicationStatusChoices.STATUS_ACTIVE,
                environment=ApplicationEnvironmentChoices.STAGING,
                criticality=ApplicationCriticalityChoices.MEDIUM
            ),
            Application(
                name='DB App 1',
                slug='db-app-1',
                group=application_groups[1],
                tenant=tenants[1],
                status=ApplicationStatusChoices.STATUS_PLANNED,
                environment=ApplicationEnvironmentChoices.PRODUCTION,
                criticality=ApplicationCriticalityChoices.CRITICAL
            ),
        )
        Application.objects.bulk_create(applications)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'name': 'New Application',
            'slug': 'new-application',
            'group': application_groups[1].pk,
            'tenant': tenants[1].pk,
            'status': ApplicationStatusChoices.STATUS_ACTIVE,
            'environment': ApplicationEnvironmentChoices.DEVELOPMENT,
            'criticality': ApplicationCriticalityChoices.LOW,
            'version': '2.0.0',
            'owner': 'Jane Smith',
            'business_unit': 'Engineering',
            'description': 'New test application',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "name,slug,group,status,environment,criticality",
            f"CSV App 1,csv-app-1,{application_groups[0].pk},{ApplicationStatusChoices.STATUS_ACTIVE},{ApplicationEnvironmentChoices.PRODUCTION},{ApplicationCriticalityChoices.HIGH}",
            f"CSV App 2,csv-app-2,{application_groups[1].pk},{ApplicationStatusChoices.STATUS_PLANNED},{ApplicationEnvironmentChoices.STAGING},{ApplicationCriticalityChoices.MEDIUM}",
            f"CSV App 3,csv-app-3,{application_groups[0].pk},{ApplicationStatusChoices.STATUS_ACTIVE},{ApplicationEnvironmentChoices.DEVELOPMENT},{ApplicationCriticalityChoices.LOW}",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{applications[0].pk},Web App 1,Updated web application 1",
            f"{applications[1].pk},Web App 2,Updated web application 2",
            f"{applications[2].pk},DB App 1,Updated database application 1",
        )

        cls.bulk_edit_data = {
            'status': ApplicationStatusChoices.STATUS_STAGING,
            'criticality': ApplicationCriticalityChoices.MEDIUM,
        }


class ApplicationServerTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = ApplicationServer

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

        # 创建IP地址
        ip_addresses = (
            IPAddress(address='192.168.1.100/24'),
            IPAddress(address='192.168.1.101/24'),
        )
        IPAddress.objects.bulk_create(ip_addresses)

        # 创建应用服务器
        application_servers = (
            ApplicationServer(
                application=applications[0],
                device=devices[0],
                name='Web Server 1',
                role=ServerRoleChoices.WEB_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE,
                primary_ip4=ip_addresses[0]
            ),
            ApplicationServer(
                application=applications[0],
                virtual_machine=virtual_machines[0],
                name='App Server 1',
                role=ServerRoleChoices.APPLICATION_SERVER,
                status=ServerStatusChoices.STATUS_ACTIVE,
                primary_ip4=ip_addresses[1]
            ),
            ApplicationServer(
                application=applications[1],
                device=devices[1],
                name='DB Server 1',
                role=ServerRoleChoices.DATABASE_SERVER,
                status=ServerStatusChoices.STATUS_PLANNED
            ),
        )
        ApplicationServer.objects.bulk_create(application_servers)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'application': applications[1].pk,
            'device': devices[1].pk,
            'name': 'New Server',
            'role': ServerRoleChoices.CACHE_SERVER,
            'status': ServerStatusChoices.STATUS_ACTIVE,
            'cpu_cores': 8,
            'memory_gb': 16,
            'storage_gb': 500,
            'operating_system': 'CentOS 8',
            'middleware': 'Redis',
            'description': 'New cache server',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "application,name,role,status",
            f"{applications[0].pk},CSV Server 1,{ServerRoleChoices.WEB_SERVER},{ServerStatusChoices.STATUS_ACTIVE}",
            f"{applications[1].pk},CSV Server 2,{ServerRoleChoices.APPLICATION_SERVER},{ServerStatusChoices.STATUS_PLANNED}",
            f"{applications[0].pk},CSV Server 3,{ServerRoleChoices.DATABASE_SERVER},{ServerStatusChoices.STATUS_ACTIVE}",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{application_servers[0].pk},Web Server 1,Updated web server",
            f"{application_servers[1].pk},App Server 1,Updated app server",
            f"{application_servers[2].pk},DB Server 1,Updated database server",
        )

        cls.bulk_edit_data = {
            'status': ServerStatusChoices.STATUS_OFFLINE,
            'operating_system': 'Ubuntu 22.04',
        }


class ApplicationEndpointTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = ApplicationEndpoint

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
                name='Web UI',
                type=EndpointTypeChoices.WEB_UI,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                url='https://webapp1.example.com',
                is_public=True,
                ssl_enabled=True
            ),
            ApplicationEndpoint(
                application=applications[0],
                server=servers[0],
                name='Admin Panel',
                type=EndpointTypeChoices.WEB_UI,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                ip_address=ip_addresses[0],
                port=8080,
                path='/admin'
            ),
            ApplicationEndpoint(
                application=applications[1],
                server=servers[1],
                name='REST API',
                type=EndpointTypeChoices.API,
                status=EndpointStatusChoices.STATUS_ACTIVE,
                url='https://api.example.com/v1',
                is_public=True,
                authentication_required=True
            ),
        )
        ApplicationEndpoint.objects.bulk_create(application_endpoints)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'application': applications[1].pk,
            'server': servers[1].pk,
            'name': 'GraphQL API',
            'type': EndpointTypeChoices.API,
            'status': EndpointStatusChoices.STATUS_ACTIVE,
            'url': 'https://api.example.com/graphql',
            'is_public': True,
            'authentication_required': True,
            'ssl_enabled': True,
            'documentation_url': 'https://docs.example.com/graphql',
            'description': 'GraphQL API endpoint',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "application,name,type,status",
            f"{applications[0].pk},CSV Endpoint 1,{EndpointTypeChoices.WEB_UI},{EndpointStatusChoices.STATUS_ACTIVE}",
            f"{applications[1].pk},CSV Endpoint 2,{EndpointTypeChoices.API},{EndpointStatusChoices.STATUS_PLANNED}",
            f"{applications[0].pk},CSV Endpoint 3,{EndpointTypeChoices.DATABASE},{EndpointStatusChoices.STATUS_ACTIVE}",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{application_endpoints[0].pk},Web UI,Updated web interface",
            f"{application_endpoints[1].pk},Admin Panel,Updated admin panel",
            f"{application_endpoints[2].pk},REST API,Updated REST API",
        )

        cls.bulk_edit_data = {
            'status': EndpointStatusChoices.STATUS_MAINTENANCE,
            'is_public': False,
        }


class ApplicationPersonnelTestCase(ViewTestCases.PrimaryObjectViewTestCase):
    model = ApplicationPersonnel

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
                department='IT',
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
                department='IT',
                title='System Administrator',
                start_date=date(2023, 3, 1)
            ),
        )
        ApplicationPersonnel.objects.bulk_create(application_personnel)

        tags = create_tags('Alpha', 'Bravo', 'Charlie')

        cls.form_data = {
            'application': applications[1].pk,
            'contact': contacts[1].pk,
            'name': 'Bob Wilson',
            'role': PersonnelRoleChoices.TESTER,
            'email': 'bob.wilson@example.com',
            'phone': '+1122334455',
            'department': 'QA',
            'title': 'QA Engineer',
            'is_primary': False,
            'is_emergency_contact': False,
            'start_date': '2024-01-01',
            'notes': 'Responsible for testing',
            'description': 'QA team member',
            'tags': [t.pk for t in tags],
        }

        cls.csv_data = (
            "application,name,role,email",
            f"{applications[0].pk},CSV Person 1,{PersonnelRoleChoices.DEVELOPER},csv1@example.com",
            f"{applications[1].pk},CSV Person 2,{PersonnelRoleChoices.OPERATOR},csv2@example.com",
            f"{applications[0].pk},CSV Person 3,{PersonnelRoleChoices.SUPPORT},csv3@example.com",
        )

        cls.csv_update_data = (
            "id,name,description",
            f"{application_personnel[0].pk},John Doe,Updated owner",
            f"{application_personnel[1].pk},Jane Smith,Updated developer",
            f"{application_personnel[2].pk},John Doe,Updated administrator",
        )

        cls.bulk_edit_data = {
            'department': 'Updated Department',
            'is_emergency_contact': True,
        }