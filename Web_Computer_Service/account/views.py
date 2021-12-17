from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django.utils.crypto import get_random_string
from django.contrib import messages
from .forms import EmployeeCreationForm, CustomerCreationForm
from .models import User

def main(request):
    return render(request, 'index.html')

class LoginPage(LoginView):
    template_name = "account/index.html"

class ServiceMainPage(TemplateView):
    template_name = 'service.html'


def create_employee(request):
    if request.method == "POST":
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.is_employee = 1
            random_password = get_random_string(10, "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
            new_employee.set_password(random_password)
            new_employee.save()
            contex = {
                'user': new_employee,
                'password': random_password
                }
            return render(request, 'service_functions/employee_create_complete.html', contex)

    else:
        form = EmployeeCreationForm()
    return render(request, 'service_functions/add_employee.html', {'form': form})

def edit_employee_object(request, id):
    employee = get_object_or_404(User, pk=id)
    employee_password = employee.password
    form = EmployeeCreationForm(request.POST or None, instance = employee)
    
    if form.is_valid():
        employee_temp = form.save(commit=False)
        employee_temp.set_password(employee_password)
        employee_temp.save()
        messages.success(request, 'Konto pomyślnie zaktualizowane')
        return redirect('Web_Computer_Service:service')

    return render(request, 'service_functions/edit_employee_object_instance.html', {'form': form})

def create_customer(request):
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            new_customer = form.save(commit=False)
            new_customer.is_customer = 1
            random_password = get_random_string(10, "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
            new_customer.set_password(random_password)
            new_customer.save()
            contex = {
                'user': new_customer,
                'password': random_password
                }
            return render(request, 'service_functions/employee_create_complete.html', contex)

    else:
        form = CustomerCreationForm()
    return render(request, 'service_functions/add_customer.html', {'form': form})


def edit_employee(request):
    data = User.objects.filter(is_employee=True)
    return render(request, 'service_functions/edit_employee.html', {'user': data})
