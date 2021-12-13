from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView


# def main(request):
#     return render(request, 'index.html')

class MainPage(LoginView):
    template_name = "account/index.html"

class ServiceMainPage(TemplateView):
    template_name = 'service.html'