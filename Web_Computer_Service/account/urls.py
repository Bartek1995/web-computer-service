from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "Web_Computer_Service"

urlpatterns = [
    path('', views.login_page, name="login"),
    path('service/logout', LogoutView.as_view(), name="logout"),
    path('service', views.service_main_page, name="service"),
    path('service/create_order', views.create_order, name="create_order"),
    path('service/order_management/<int:id>', views.order_management, name="order_management"),
    path('service/order_management/order_information', views.order_information, name="order_information"),
    # path('service/order_management/order_information_data', views.order_information_data, name="order_information_data"),
    path('service/order_management/<int:id>/delete_order_ask', views.delete_order_ask, name="delete_order_ask"),
    path('service/order_management/<int:id>/delete_order_confirmation', views.delete_order_confirmation, name="delete_order_confirmation"),
    path('service/order_management/<int:id>/delete_order_cancel', views.delete_order_cancel, name="delete_order_cancel"),
    path('service/order_management/<int:id>/modify_description', views.modify_description, name="modify_description"),
    path('service/order_management/<int:id>/modify_order_state', views.modify_order_state, name="modify_order_state"),
    path('service/order_management/<int:id>/add_device_to_order', views.add_device_to_order, name="add_device_to_order"),
    path('service/order_list', views.order_list, name="order_list"),
    path('service/clean_order_cookies', views.clean_order_cookies, name="clean_order_cookies"),
    path('service/create_employee', views.create_employee, name='create_employee'),
    path('service/create_customer', views.create_customer, name='create_customer'),
    path('service/customer_list', views.customer_list, name='customer_list'),
    path('service/edit_employee', views.edit_employee, name='edit_employee'),
    path('service/edit_employee_object/<int:id>', views.edit_employee_object, name='edit_employee_object'),
    path('service/delete_employee_ask/<int:id>', views.delete_employee_ask, name='delete_employee_ask'),
    path('service/delete_employee_cancel', views.delete_employee_cancel, name='delete_employee_cancel'),
    path('service/delete_employee_confirmation/<int:id>', views.delete_employee_confirmation, name='delete_employee_confirmation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
