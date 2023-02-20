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
        blank=True,
        upload_to='recipes/',
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
        through='RecipesTags',
        verbose_name='Теги'
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

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиента'
        ordering = ('-ingredient',)

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class RecipesTags(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    tags = models.ForeignKey(
        Tags,
        verbose_name='Тег',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-tags',)

    def __str__(self):
        return f'У рецепта {self.recipe} есть {self.tags}'
