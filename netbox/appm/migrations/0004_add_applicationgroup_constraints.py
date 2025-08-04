from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('appm', '0003_fix_applicationgroup_mptt'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='applicationgroup',
            constraint=models.UniqueConstraint(
                fields=('parent', 'name'),
                name='appm_applicationgroup_unique_parent_name'
            ),
        ),
    ]