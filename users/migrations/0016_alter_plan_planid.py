# Generated by Django 3.2.14 on 2022-09-18 10:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_plan_planid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='planID',
            field=models.UUIDField(default=uuid.UUID('4a66195e-35a8-4155-9437-c627342e5611'), primary_key=True, serialize=False),
        ),
    ]
