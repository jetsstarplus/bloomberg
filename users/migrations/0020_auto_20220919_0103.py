# Generated by Django 3.2.14 on 2022-09-18 22:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_plan_planid'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='period',
            field=models.IntegerField(default=1, verbose_name='product ordered renewal period in months'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='planID',
            field=models.UUIDField(default=uuid.UUID('9d43975a-faec-4c8d-8afa-a22d577a56d7'), editable=False, primary_key=True, serialize=False),
        ),
    ]
