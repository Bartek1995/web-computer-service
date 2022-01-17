# Generated by Django 3.2.9 on 2021-12-17 19:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_number',
            field=models.ForeignKey(limit_choices_to={'is_customer': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
