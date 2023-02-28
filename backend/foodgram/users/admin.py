from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import User, Follower


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


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    ordering = ("user",)
    empty_value_display = '-пусто-'
