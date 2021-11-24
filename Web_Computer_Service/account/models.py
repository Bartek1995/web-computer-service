from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.utils import timezone
# Create your models here.

class User (AbstractUser): 
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Employee (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    salary = models.SmallIntegerField(blank=True, null=True)
    department = models.CharField(blank=False, max_length=20, default="Brak danych")

class Customer (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birth_date = models.DateField(null=True)
    account_create_date = models.DateTimeField(default=timezone.now)