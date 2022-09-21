# Generated by Django 3.2.14 on 2022-09-18 21:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('filesManager', '0007_auto_20220919_0038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='numberseries',
            options={'verbose_name': 'Number Series', 'verbose_name_plural': 'Number Series'},
        ),
        migrations.AlterField(
            model_name='files',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('e555184c-f16e-4236-bba7-47376d091ed7'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='ID',
            field=models.UUIDField(default=uuid.UUID('552ee0d8-c17a-465d-b973-5e5857e7e83f'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='numberseries',
            name='last_no_used',
            field=models.CharField(editable=False, max_length=50),
        ),
    ]
