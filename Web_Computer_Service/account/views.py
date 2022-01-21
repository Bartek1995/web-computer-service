from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.base import TemplateView
from django.utils.crypto import get_random_string
from django.contrib import messages
from .forms import AddDeviceToOrder, EmployeeCreationForm, CustomerCreationForm, OrderCreateForm, AddDescriptionToOrder, AddOrderStateToOrder
from .models import OrderDevice, User, Order

def main(request):
    return render(request, 'index.html')

class LoginPage(LoginView):
    template_name = "account/index.html"

def service_main_page(request):
    return render (request, 'service.html')

# --------------USER MANAGEMENT--------------

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
        employee_temp.is_employee = 1
        employee_temp.set_password(employee_password)
        employee_temp.save()
        messages.success(request, 'Konto pomyślnie zaktualizowane')
        return redirect('Web_Computer_Service:service')

    return render(request, 'service_functions/edit_employee_object_instance.html', {'form': form})

def delete_employee_ask(request, id):
    employee = get_object_or_404(User, pk=id)
    return render(request, 'service_functions/delete_employee_ask.html', {'user': employee})

def delete_employee_confirmation(request, id):
    employee = get_object_or_404(User, pk=id)
    employee.delete()
    messages.success(request, 'Konto zostało usunięte')
    return redirect('Web_Computer_Service:service')
    
def delete_employee_cancel(request):
    messages.info(request, 'Anulowano usuwanie konta')
    return redirect('Web_Computer_Service:service')

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
            return render(request, 'service_functions/customer_create_complete.html', contex)

    else:
        form = CustomerCreationForm()
    return render(request, 'service_functions/add_customer.html', {'form': form})


def edit_employee(request):
    data = User.objects.filter(is_employee=True)
    return render(request, 'service_functions/edit_employee.html', {'user': data})



# --------------------------ORDER MANAGEMENT------------------------------

def create_order(request):
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        data_from_form = form.save(commit=False)
        try:
            User.objects.get(id=data_from_form.customer_number, is_customer = 1)
        except User.DoesNotExist:
            request.session['customer_number'] = form.cleaned_data['customer_number']
            request.session['error_text'] = "Brak klienta o takim numerze konta, sprawdź poprawność danych lub wyczyść formularz i spróbuj ponownie."
            return redirect('Web_Computer_Service:create_order')
        else:
            if form.is_valid():
                Order_object = form.save(commit=False)
                form.save()
                messages.success(request, 'Utworzono nowe zlecenie')
                return render (request, 'service_functions/order_management_ask.html', {'Order' : Order_object})
    else:
        if 'customer_number' in request.session:
            initial_form_data_from_session = {
                'customer_number' : request.session['customer_number'],
            }
            form = OrderCreateForm(initial=initial_form_data_from_session)
        else:
            form = OrderCreateForm()
    if 'error_text' in request.session:
        return render (request, 'service_functions/create_order.html', {'form' : form, 'error' : request.session['error_text']})
    else:
        return render (request, 'service_functions/create_order.html', {'form' : form})

def order_management_ask(request):
    return render (request, 'service_functions/order_management_ask.html')


def set_number_of_order_state_as_string(order_state_number):
        match order_state_number:
            case 0:
                order_state = "W trakcie weryfikacji"
            case 1:
                order_state = "Zaakceptowano"
            case 2:
                order_state = "W trakcie naprawy"
            case 3:
                order_state = "Ukończono"
        return order_state
def modify_order_device_list_category_as_string(device_list):
    for key in device_list:
        match key.category:
            case 0:
                key.category = "Podzespoły komputerowe"
            case 1:
                key.category = "Monitory"
            case 2:
                key.category = "Klawiatury i myszki"
            case 3:
                key.category = "Dyski i nośniki danych"
            case 4:
                key.category = "Słuchawki"
            case 5:
                key.category = "Drukarki i skanery"
            case 6:
                key.category = "Kable i akcesoria"
            case 7:
                key.category = "Inne"
            case 8:
                key.category = "Nie przypisano"
    return device_list

def order_management(request, id):
    try:
        del request.session['confirmation']
    except:
        pass
    order = get_object_or_404(Order, pk=id)
    order_device_list = OrderDevice.objects.all().filter(order_number=order.id)
    user = User.objects.get(pk = order.customer_number)

    order_state_as_string = set_number_of_order_state_as_string(order.order_state)
    order_device_list = modify_order_device_list_category_as_string(order_device_list)


    
    context = {
        'order' : order,
        'order_state' : order_state_as_string,
        'user' : user,
        'order_device_list' : order_device_list,
        }
    return render (request, 'service_functions/order_management.html', context)


def modify_description (request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == "POST":
        form = AddDescriptionToOrder(request.POST)
        if form.is_valid():
            order.description = form.cleaned_data['description']
            request.session['confirmation'] = "Zaktualizowano dane"
            order.save()
    else:
        form = AddDescriptionToOrder(instance = order)
    context = {
        'form' : form,
        'order' : order,
    }

    if 'confirmation' in request.session:
        context['confirmation'] = request.session['confirmation']
        return render (request, 'service_functions/add_description_to_order.html', context, )
    else:
        return render(request, 'service_functions/add_description_to_order.html', context  )


def modify_order_state (request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == "POST":
        form = AddOrderStateToOrder(request.POST)
        if form.is_valid():
            order.order_state = form.cleaned_data['order_state']
            request.session['confirmation'] = "Zaktualizowano dane" 
            order.save()
    else:
        initial_data= {
        'order_state' : order.order_state
        }
        form = AddOrderStateToOrder(initial = initial_data)
    context = {
        'form' : form,
        'order' : order,
    }

    if 'confirmation' in request.session:
        context['confirmation'] = request.session['confirmation']
        return render (request, 'service_functions/modify_order_state.html', context, )
    else:
        return render(request, 'service_functions/modify_order_state.html', context  )

def modify_order_state (request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == "POST":
        form = AddOrderStateToOrder(request.POST)
        if form.is_valid():
            order.order_state = form.cleaned_data['order_state']
            request.session['confirmation'] = "Zaktualizowano dane" 
            order.save()
    else:
        initial_data= {
        'order_state' : order.order_state
        }
        form = AddOrderStateToOrder(initial = initial_data)
    context = {
        'form' : form,
        'order' : order,
    }

    if 'confirmation' in request.session:
        context['confirmation'] = request.session['confirmation']
        return render (request, 'service_functions/modify_order_state.html', context, )
    else:
        return render(request, 'service_functions/modify_order_state.html', context  )

def add_device_to_order (request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == "POST":
        form = AddDeviceToOrder(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.order_number = id
            form_object.save()
    else:
        form = AddDeviceToOrder()
    context = {
        'form' : form,
        'order' : order
    }
    return render(request, 'service_functions/add_device_to_order.html', context)
    

def clean_order_cookies(request):
    try:
        del request.session['error_text']
        del request.session['customer_number']
        del request.session['order_state']
        del request.session['description']
    except KeyError:
        messages.info(request, "Formularz został wyczyszczony")
    finally:
        return redirect('Web_Computer_Service:create_order')
        
    
def order_list(request):
    orders = Order.objects.all()
    for element in orders:
        user_object = User.objects.get(id = element.customer_number)
        element.order_state = set_number_of_order_state_as_string(element.order_state)
        element.first_name = user_object.first_name
        element.last_name = user_object.last_name
    
    return render(request, 'service_functions/order_list.html',{'order' : orders} )