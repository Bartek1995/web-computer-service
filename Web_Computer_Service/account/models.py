from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.utils import timezone
from phone_field import PhoneField

# Create your models here.

class User (AbstractUser): 
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    address = models.CharField(max_length=50)
    phone = PhoneField(blank=True, help_text="Telefon kontaktowy")
    employee_account_number = models.IntegerField(null=True)
    customer_account_number = models.IntegerField(null=True)
    account_create_date = models.DateTimeField(auto_now_add = True)

class Order(models.Model):
    ORDER_STATUS = (
        (0, "W trakcie weryfikacji"),
        (1, "Zaakceptowano"),
        (2, "W trakcie naprawy"),
        (3, "Ukończono")
    )
    customer_number = models.IntegerField(blank=True)
    order_state = models.IntegerField(default=0, choices=ORDER_STATUS)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)

