from django.contrib import admin
from tags.models import Tags


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'
