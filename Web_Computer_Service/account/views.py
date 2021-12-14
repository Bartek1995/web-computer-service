from django.forms.forms import Form
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from .forms import EmployeeCreationForm


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
            return render(request, 'service_functions/employee_create_complete.html', {'user': new_employee})

    else:
        form = EmployeeCreationForm()
    return render(request, 'service_functions/add_employee.html', {'form': form})
