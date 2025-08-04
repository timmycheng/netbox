from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from utilities.json import CustomFieldJSONEncoder
import utilities.fields
import utilities.ordering


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dcim', '0209_device_component_denorm_site_location'),
        ('virtualization', '0048_populate_mac_addresses'),
        ('tenancy', '0020_remove_contactgroupmembership'),
        ('extras', '0129_fix_script_paths'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationGroup',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=CustomFieldJSONEncoder)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=CustomFieldJSONEncoder)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                (
                    '_name',
                    utilities.fields.NaturalOrderingField(
                        'name', blank=True, max_length=100, naturalize_function=utilities.ordering.naturalize
                    ),
                ),
                ('slug', models.SlugField(max_length=100)),
                ('status', models.CharField(default='active', max_length=50)),
                ('version', models.CharField(blank=True, max_length=50)),
                ('owner', models.CharField(blank=True, max_length=100)),
                ('business_unit', models.CharField(blank=True, max_length=100)),
                ('criticality', models.CharField(blank=True, max_length=50)),
                ('environment', models.CharField(default='production', max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('group', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='applications',
                    to='appm.applicationgroup'
                )),
                ('tenant', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='applications',
                    to='tenancy.tenant'
                )),
            ],
            options={
                'ordering': ('_name',),
            },
        ),
        migrations.CreateModel(
            name='ApplicationServer',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=CustomFieldJSONEncoder)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                (
                    '_name',
                    utilities.fields.NaturalOrderingField(
                        'name', blank=True, max_length=100, naturalize_function=utilities.ordering.naturalize
                    ),
                ),
                ('role', models.CharField(blank=True, max_length=50)),
                ('status', models.CharField(default='active', max_length=50)),
                ('cpu_cores', models.PositiveIntegerField(blank=True, null=True)),
                ('memory_gb', models.PositiveIntegerField(blank=True, null=True)),
                ('storage_gb', models.PositiveIntegerField(blank=True, null=True)),
                ('operating_system', models.CharField(blank=True, max_length=100)),
                ('middleware', models.TextField(blank=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('application', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='servers',
                    to='appm.application'
                )),
                ('device', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='application_servers',
                    to='dcim.device'
                )),
                ('virtual_machine', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='application_servers',
                    to='virtualization.virtualmachine'
                )),
            ],
            options={
                'ordering': ('application', '_name'),
            },
        ),
        migrations.CreateModel(
            name='ApplicationEndpoint',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=CustomFieldJSONEncoder)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                (
                    '_name',
                    utilities.fields.NaturalOrderingField(
                        'name', blank=True, max_length=100, naturalize_function=utilities.ordering.naturalize
                    ),
                ),
                ('type', models.CharField(default='web', max_length=50)),
                ('status', models.CharField(default='active', max_length=50)),
                ('url', models.URLField(blank=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('port', models.PositiveIntegerField(
                    blank=True,
                    null=True,
                    validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(65535)]
                )),
                ('protocol', models.CharField(blank=True, max_length=20)),
                ('path', models.CharField(blank=True, max_length=200)),
                ('is_public', models.BooleanField(default=False)),
                ('is_load_balanced', models.BooleanField(default=False)),
                ('health_check_url', models.URLField(blank=True)),
                ('authentication_required', models.BooleanField(default=True)),
                ('ssl_enabled', models.BooleanField(default=False)),
                ('documentation_url', models.URLField(blank=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('comments', models.TextField(blank=True)),
                ('application', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='endpoints',
                    to='appm.application'
                )),
                ('server', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='endpoints',
                    to='appm.applicationserver'
                )),
            ],
            options={
                'ordering': ('application', '_name'),
            },
        ),
        migrations.CreateModel(
            name='ApplicationPersonnel',
            fields=[
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=CustomFieldJSONEncoder)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                (
                    '_name',
                    utilities.fields.NaturalOrderingField(
                        'name', blank=True, max_length=100, naturalize_function=utilities.ordering.naturalize
                    ),
                ),
                ('role', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('is_primary', models.BooleanField(default=False)),
                ('is_emergency_contact', models.BooleanField(default=False)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('application', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='personnel',
                    to='appm.application'
                )),
                ('contact', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='application_personnel',
                    to='tenancy.contact'
                )),
            ],
            options={
                'ordering': ('application', '_name'),
                'verbose_name_plural': 'application personnel',
            },
        ),
        migrations.AddConstraint(
            model_name='application',
            constraint=models.UniqueConstraint(
                fields=('name', 'environment'),
                name='appm_application_unique_name_environment'
            ),
        ),
        migrations.AddConstraint(
            model_name='applicationserver',
            constraint=models.UniqueConstraint(
                fields=('application', 'name'),
                name='appm_applicationserver_unique_application_name'
            ),
        ),
        migrations.AddConstraint(
            model_name='applicationendpoint',
            constraint=models.UniqueConstraint(
                fields=('application', 'name'),
                name='appm_applicationendpoint_unique_application_name'
            ),
        ),
        migrations.AddConstraint(
            model_name='applicationpersonnel',
            constraint=models.UniqueConstraint(
                fields=('application', 'name', 'role'),
                name='appm_applicationpersonnel_unique_application_name_role'
            ),
        ),
    ]