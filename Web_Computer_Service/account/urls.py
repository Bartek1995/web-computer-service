from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from .views import LoginPage, delete_employee_ask, order_list
from django.conf import settings
from django.conf.urls.static import static
app_name = "Web_Computer_Service"

urlpatterns = [
    path('', LoginPage.as_view(), name="login"),
    path('', LogoutView.as_view(), name="logout"),
    path('service', views.service_main_page, name="service"),
    path('service/create_order', views.create_order, name="create_order"),
    path('service/order_management/<int:id>', views.order_management, name="order_management"),
    path('service/order_management/<int:id>/modify_description', views.modify_description, name="modify_description"),
    path('service/order_management/<int:id>/modify_order_state', views.modify_order_state, name="modify_order_state"),
    path('service/order_list', views.order_list, name="order_list"),
    path('service/clean_order_cookies', views.clean_order_cookies, name="clean_order_cookies"),
    path('service/create_employee', views.create_employee, name='create_employee'),
    path('service/create_customer', views.create_customer, name='create_customer'),
    path('service/edit_employee', views.edit_employee, name='edit_employee'),
    path('service/edit_employee_object/<int:id>', views.edit_employee_object, name='edit_employee_object'),
    path('service/delete_employee_ask/<int:id>', views.delete_employee_ask, name='delete_employee_ask'),
    path('service/delete_employee_cancel', views.delete_employee_cancel, name='delete_employee_cancel'),
    path('service/delete_employee_confirmation/<int:id>', views.delete_employee_confirmation, name='delete_employee_confirmation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
