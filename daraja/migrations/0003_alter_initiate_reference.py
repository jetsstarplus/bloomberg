# Generated by Django 3.2.14 on 2022-09-20 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daraja', '0002_initiate_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='initiate',
            name='reference',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
