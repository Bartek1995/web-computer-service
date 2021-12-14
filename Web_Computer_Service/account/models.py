from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from django.utils import timezone
# Create your models here.

class User (AbstractUser): 
    is_employee = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    address = models.CharField(max_length=50, default="Brak")
    employee_account_number = models.IntegerField(null=True)
    # account_create_date = models.DateTimeField(default=timezone.now)