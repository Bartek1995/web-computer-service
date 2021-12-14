from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import MainPage, ServiceMainPage
app_name = "Web_Computer_Service"

urlpatterns = [
    path('', MainPage.as_view(), name="main"),
    path('service', ServiceMainPage.as_view(), name="service"),
    path('service/create_employee', views.create_employee, name='create_employee'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
