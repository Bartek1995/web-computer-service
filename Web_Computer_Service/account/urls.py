from django.urls import path
from . import views

app_name = "Web_Computer_Service"

urlpatterns = [
    path('', views.main, name="main")
]
