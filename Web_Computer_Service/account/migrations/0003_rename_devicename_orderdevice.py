# Generated by Django 3.2.9 on 2022-01-21 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_devicename'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeviceName',
            new_name='OrderDevice',
        ),
    ]
