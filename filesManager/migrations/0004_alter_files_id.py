# Generated by Django 3.2.14 on 2022-09-16 05:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filesManager', '0003_auto_20220916_0856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('dcc6768e-e108-42d8-984c-b4584fc9102b'), primary_key=True, serialize=False),
        ),
    ]