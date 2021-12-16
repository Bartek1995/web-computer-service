from django.forms.forms import Form
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django.utils.crypto import get_random_string
from .forms import EmployeeCreationForm
from .models import User

def main(request):
    return render(request, 'index.html')

class MainPage(LoginView):
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


def edit_employee(request):
    data = User.objects.filter(is_employee=True)
    return render(request, 'service_functions/edit_employee.html', {'user': data})
