from django.contrib import admin
from django.contrib.admin import display
from recipes.models import Favorite, Recipes, RecipesIngredient, ShoppingCart


class RecipesIngredientInLine(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


class RecipesTagInLines(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'
    inlines = (RecipesIngredientInLine, RecipesTagInLines)

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(RecipesIngredient)
class RecipesIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'
