from django.contrib import admin

from recipes.models import Recipes, RecipesIngredient, RecipesTags
from tags.models import Tags


class RecipesIngredientInLine(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


class RecipesTagsInLines(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1

@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'cooking_time')
    empty_value_display = '-пусто-'
    inlines = (RecipesIngredientInLine, RecipesTagsInLines)


@admin.register(RecipesIngredient)
class RecipesIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'


