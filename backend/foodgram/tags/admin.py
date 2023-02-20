from django.contrib import admin
from tags.models import Tags


class TagsAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


admin.site.register(Tags)
