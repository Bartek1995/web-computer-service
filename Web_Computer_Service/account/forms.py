from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User
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
        fields = ['username', 'email', 'phone', 'employee_account_number','is_employee']

        labels = {
            'username': "Nazwa użytkownika",
            'employee_account_number': "Numer pracownika",
        }

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
        fields = ['username', 'email', 'phone', 'customer_account_number','is_customer']

        labels = {
            'username': "Nazwa użytkownika",
            'customer_account_number': "Numer klienta",
        }

    