# Generated by Django 3.2.14 on 2022-09-20 07:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filesManager', '0012_auto_20220920_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('49522212-70d9-4c59-af96-b1f523f9444c'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('27262b10-54cd-4d4d-b2f4-3e60250829f7'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='last_no_used',
            field=models.IntegerField(default=0, verbose_name='Last Used Number'),
        ),
    ]
