# Generated by Django 3.2.9 on 2021-12-16 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_employee_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='customer_account_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='Brak informacji', max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(default='Brak informacji', max_length=50),
        ),
    ]
