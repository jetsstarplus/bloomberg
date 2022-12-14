# Generated by Django 3.2.14 on 2022-09-18 13:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filesManager', '0005_auto_20220918_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('2269120e-f16c-4f69-b4a7-5cb42c10f64d'), primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='files',
            name='file',
            field=models.FileField(null=True, upload_to='files'),
        ),
    ]
