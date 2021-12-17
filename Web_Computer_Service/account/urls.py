from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import LoginPage
from django.conf import settings
from django.conf.urls.static import static
from .views import ServiceMainPage
app_name = "Web_Computer_Service"

urlpatterns = [
    path('', LoginPage.as_view(), name="login"),
    path('', LogoutView.as_view(), name="logout"),
    path('service', ServiceMainPage.as_view(), name="service"),
    path('service/create_employee', views.create_employee, name='create_employee'),
    path('service/create_customer', views.create_customer, name='create_customer'),
    path('service/edit_employee', views.edit_employee, name='edit_employee'),
    path('service/edit_employee_object/<int:id>', views.edit_employee_object, name='edit_employee_object'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
