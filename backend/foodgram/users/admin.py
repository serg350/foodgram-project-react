from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Follower, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'username',
        'id',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = ('email', 'first_name')
    empty_value_display = '-пусто-'


@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    list_editable = ('user', 'author')
    ordering = ("user",)
    empty_value_display = '-пусто-'
