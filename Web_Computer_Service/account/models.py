from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
# Create your models here.

class User (AbstractUser): 
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Employee (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneField(blank=True)

class Customer (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = PhoneField(blank=False)