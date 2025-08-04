from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('appm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationgroup',
            name='comments',
            field=models.TextField(blank=True),
        ),
    ]