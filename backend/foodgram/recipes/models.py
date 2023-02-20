from django.db import models
from django.conf import settings

from tags.models import Tags
from ingredients.models import Ingredients


class Recipes(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления блюда'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    #author = models.ForeignKey(
    #    settings.AUTH_USER_MODEL,
    #    on_delete=models.CASCADE,
    #    verbose_name='Автор',
    #)
    tags = models.ManyToManyField(
        Tags,
        verbose_name='Теги',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngredient',
        verbose_name='Ингридиенты'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class RecipesIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        verbose_name='Ингридиенты',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Количество ингредиента'
    )
