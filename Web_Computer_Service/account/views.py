from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib import messages
from django.contrib.auth.models import Group
from .decorators import allowed_users
from .forms import AddDeviceToOrder, EmployeeCreationForm, GetOrderInformation, LoginForm, CustomerCreationForm, OrderCreateForm, AddDescriptionToOrder, AddOrderStateToOrder
from .models import OrderDevice, User, Order



def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Zalogowano pomyślnie')
                return redirect('Web_Computer_Service:service')
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form' : form })


@login_required(login_url='/main/')
def service_main_page(request):
    return render (request, 'service.html')

# --------------USER MANAGEMENT--------------


@allowed_users(allowed_groups=['admin'])
def create_employee(request):
    if request.method == "POST":
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            new_employee = form.save(commit=False)
            new_employee.is_employee = 1
            random_password = get_random_string(10, "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
            new_employee.set_password(random_password)
            new_employee.save()
            group = Group.objects.get(name='employee')
            new_employee.groups.add(group)
            contex = {
                'new_user': new_employee,
                'password': random_password
                }
            return render(request, 'service_functions/employee_create_complete.html', contex)

    else:
        form = EmployeeCreationForm()
    return render(request, 'service_functions/add_employee.html', {'form': form})

@allowed_users(allowed_groups=['admin'])
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

@allowed_users(allowed_groups=['admin'])
def delete_employee_ask(request, id):
    employee = get_object_or_404(User, pk=id)
    return render(request, 'service_functions/delete_employee_ask.html', {'user': employee})


@allowed_users(allowed_groups=['admin'])
def delete_employee_confirmation(request, id):
    employee = get_object_or_404(User, pk=id)
    employee.delete()
    messages.success(request, 'Konto zostało usunięte')
    return redirect('Web_Computer_Service:service')

@allowed_users(allowed_groups=['admin'])
def delete_employee_cancel(request):
        messages.info(request, 'Anulowano usuwanie konta')
        return redirect('Web_Computer_Service:service')


@allowed_users(allowed_groups=['employee'])
def create_customer(request):
    if request.method == "POST":
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            new_customer = form.save(commit=False)
            new_customer.is_customer = 1
            random_password = get_random_string(10, "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789")
            new_customer.set_password(random_password)
            new_customer.save()
            group = Group.objects.get(name='customer')
            new_customer.groups.add(group)
            contex = {
                'new_user': new_customer,
                'password': random_password
                }
            return render(request, 'service_functions/customer_create_complete.html', contex)

    else:
        form = CustomerCreationForm()
    return render(request, 'service_functions/add_customer.html', {'form': form})

@allowed_users(allowed_groups=['admin'])
def edit_employee(request):
    data = User.objects.filter(is_employee=True)
    return render(request, 'service_functions/edit_employee.html', {'data': data})

@allowed_users(allowed_groups=['admin', 'employee'])
def customer_list(request):
    data = User.objects.filter(is_customer=True)
    return render(request, 'service_functions/customer_list.html', {'data': data})



# --------------------------ORDER MANAGEMENT------------------------------
@allowed_users(allowed_groups=['employee'])
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

@allowed_users(allowed_groups=['employee'])
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

@allowed_users(allowed_groups=['employee'])
def order_management(request, id):
    try:
        del request.session['confirmation']
    except:
        pass
    order = get_object_or_404(Order, pk=id)
    order_device_list = OrderDevice.objects.all().filter(order_number=order.id)
    user_from_order = User.objects.get(pk = order.customer_number)

    order_state_as_string = set_number_of_order_state_as_string(order.order_state)
    order_device_list = modify_order_device_list_category_as_string(order_device_list)


    
    context = {
        'order' : order,
        'order_state' : order_state_as_string,
        'user_from_order' : user_from_order,
        'order_device_list' : order_device_list,
        }
    return render (request, 'service_functions/order_management.html', context)

@allowed_users(allowed_groups=['employee'])
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

@allowed_users(allowed_groups=['employee'])
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

@allowed_users(allowed_groups=['employee'])
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

@allowed_users(allowed_groups=['employee'])
def add_device_to_order (request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == "POST":
        form = AddDeviceToOrder(request.POST)
        if form.is_valid():
            form_object = form.save(commit=False)
            form_object.order_number = id
            form_object.save()
            request.session['confirmation'] = "Dodano urządzenie do zlecenia"

    else:
        form = AddDeviceToOrder()
    context = {
        'form' : form,
        'order' : order,
    }
    if 'confirmation' in request.session:
        context['confirmation'] = request.session['confirmation']
        return render (request, 'service_functions/add_device_to_order.html', context, )
    else:
        return render(request, 'service_functions/add_device_to_order.html', context  )

    

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
    if len(orders) == 0:
        messages.info(request, 'Brak zleceń w systemie')
        return redirect('Web_Computer_Service:service')

    for element in orders:
        user_object = User.objects.get(id = element.customer_number)
        element.order_state = set_number_of_order_state_as_string(element.order_state)
        element.first_name = user_object.first_name
        element.last_name = user_object.last_name

    return render(request, 'service_functions/order_list.html',{'order' : orders} )

def order_information(request):
    if request.method == 'POST':
        form = GetOrderInformation(request.POST)
        if form.is_valid():
            order_number = form.cleaned_data['order_number']
            try:
                order = Order.objects.get(id = order_number)
                devices = OrderDevice.objects.all().filter(order_number = order.id)
                order.order_state = set_number_of_order_state_as_string(order.order_state)
                devices = modify_order_device_list_category_as_string(devices)
            except:
                error = "Brak takiego zamówienia"
                return render(request,'service_functions/order_information.html', {'form' : form, 'error' : error})
            else:
                return render(request,'service_functions/order_information.html', {'form' : form, 'order': order, 'devices' : devices})


    else:
        form = GetOrderInformation()
    return render(request,'service_functions/order_information.html', {'form' : form})

        

@allowed_users(allowed_groups=['employee'])
def delete_order_ask(request, id):
    order = get_object_or_404(Order, pk=id)
    return render(request, 'service_functions/delete_order_ask.html', {'order': order})

@allowed_users(allowed_groups=['employee'])
def delete_order_confirmation(request, id):
    order = get_object_or_404(Order, pk=id)
    order_devices = OrderDevice.objects.all().filter(order_number= order.id)
    order.delete()
    order_devices.delete()
    messages.success(request, 'Zlecenie zostało usunięte')
    return redirect('Web_Computer_Service:service')
    
@allowed_users(allowed_groups=['employee'])
def delete_order_cancel(request, id):
    messages.info(request, 'Anulowano usuwanie zlecenia')
    return redirect('Web_Computer_Service:service')