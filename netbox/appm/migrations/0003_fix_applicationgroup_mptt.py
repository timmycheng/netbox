from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        ('appm', '0002_add_comments_to_applicationgroup'),
    ]

    operations = [
        # Add parent field for MPTT
        migrations.AddField(
            model_name='applicationgroup',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='appm.applicationgroup'
            ),
        ),
        # Remove unique constraint from name field
        migrations.AlterField(
            model_name='applicationgroup',
            name='name',
            field=models.CharField(max_length=100, verbose_name='name'),
        ),
        # Remove unique constraint from slug field
        migrations.AlterField(
            model_name='applicationgroup',
            name='slug',
            field=models.SlugField(max_length=100, verbose_name='slug'),
        ),
    ]