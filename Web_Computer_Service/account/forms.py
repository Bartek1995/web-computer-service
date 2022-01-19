from django.db.models import fields
from django.forms import ModelForm, models
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order
from django import forms


class EmployeeCreationForm(UserCreationForm):
    password1 = forms.CharField(
    label='Hasło',
    strip=False,
    widget=forms.PasswordInput(),
    )

    password2 = forms.CharField(
    label='Potwierdź hasło',
    strip=False,
    widget=forms.PasswordInput(),
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name','is_employee','address']

class CustomerCreationForm(UserCreationForm):
    password1 = forms.CharField(
    label='Hasło',
    strip=False,
    widget=forms.PasswordInput(),
    )

    password2 = forms.CharField(
    label='Potwierdź hasło',
    strip=False,
    widget=forms.PasswordInput(),
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name','is_customer','address']

class OrderCreateForm(ModelForm):
    customer_number = forms.IntegerField(required=True)
    class Meta:
        model = Order
        fields = ['customer_number']