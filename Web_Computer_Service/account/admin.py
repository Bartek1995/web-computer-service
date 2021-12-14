from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


# @admin.register(CustomUser)
# class AbstracUserAdmin(admin.ModelAdmin):
#     list_display = ("username", "first_name", "last_name", "email", "is_employee", "is_customer")
#     # fields = ("username", "first_name", "last_name", "email", "password")

class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(User, CustomUserAdmin)