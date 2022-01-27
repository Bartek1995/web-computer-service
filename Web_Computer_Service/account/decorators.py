from email import message
from django.shortcuts import redirect
from django.contrib import messages




# DECORATOR - IF USER IS IN ALLOWED GROUP THEN HE CAN RECIVE SELECTED VIEW

def allowed_users(allowed_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            # IF USER IS ASSIGNED TO GROUP
            if request.user.groups.exists():
                group = request.user.groups.all()
            
            for key in group:
                if key.name in allowed_groups:
                    return view_func(request, *args, **kwargs)
            else:
                #SEND ERROR TO MESSAGES IF USER IS NOT IN ALLOWED GROUP
                messages.error(request, 'Brak uprawnień do przeglądania tej strony')
                return redirect('Web_Computer_Service:service')
        return wrapper_func
    return decorator

        
