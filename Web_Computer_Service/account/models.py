from unicodedata import category
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

class OrderDevice(models.Model):
    CATEGORY_ID = (
    (0, "Podzespoły komputerowe"),
    (1, "Monitory"),
    (2, "Klawiatury i myszki"),
    (3, "Dyski i nośniki danych"),
    (4, "Słuchawki"),
    (5, "Drukarki i skanery"),
    (6, "Kable i akcesoria"),
    (7, "Inne"),
    (8, "Nie przypisano"),
    )
    order_number = models.IntegerField(blank=False)
    device_name = models.CharField(max_length=60)
    category = models.IntegerField(default=8, choices=CATEGORY_ID)

