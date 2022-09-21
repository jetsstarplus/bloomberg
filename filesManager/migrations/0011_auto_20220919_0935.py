# Generated by Django 3.2.14 on 2022-09-19 06:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filesManager', '0010_auto_20220919_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('84dea904-8d0f-4662-aea3-5db2bd65c109'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('85188ea5-2de8-4408-bd66-62b51cdcb9c8'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='prefix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='suffix',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
