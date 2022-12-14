# Generated by Django 3.2.14 on 2022-09-16 05:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20220915_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planentries',
            old_name='User',
            new_name='user',
        ),
        migrations.AddField(
            model_name='plan',
            name='current',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='plan',
            name='date_expired',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='planentries',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='planentries',
            name='transaction_no',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='plan',
            name='planID',
            field=models.UUIDField(default=uuid.UUID('907109c4-59d4-4d9e-8b82-0ec8c50b3aad'), primary_key=True, serialize=False),
        ),
    ]
