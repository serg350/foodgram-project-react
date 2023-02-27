from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'role',
        'is_active'
    )
    list_editable = ('role', 'is_active')
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'username',
    )
    list_filter = ('role', 'is_staff', 'is_active')
    empty_value_display = '-пусто-'