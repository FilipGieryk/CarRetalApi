from django.contrib import admin
from django.db import models

from django.contrib.auth.admin import UserAdmin
from .models import  Rental, CarListing, CarModel, Make, User


class CustomUserAdmin(UserAdmin):
     add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions', 'is_employee'
                )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

# admin.site.register(Employee)
admin.site.register(Rental)
# admin.site.register(Client)
admin.site.register(CarListing)
admin.site.register(CarModel)
admin.site.register(Make)
admin.site.register(User, CustomUserAdmin)
# Register your models here.
