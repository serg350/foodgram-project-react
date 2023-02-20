from django.contrib import admin

from ingredients.models import Ingredients


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'mesurment_unit')
    empty_value_display = '-пусто-'


admin.site.register(Ingredients)
