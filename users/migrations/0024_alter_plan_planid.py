# Generated by Django 3.2.14 on 2022-09-20 07:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20220920_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='planID',
            field=models.UUIDField(default=uuid.UUID('f2afef71-9ca3-44a9-b8ab-ee3812284286'), editable=False, primary_key=True, serialize=False),
        ),
    ]
