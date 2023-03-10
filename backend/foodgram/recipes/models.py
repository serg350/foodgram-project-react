from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from ingredients.models import Ingredients
from tags.models import Tags


class Recipes(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes/image',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Время приготовления блюда'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipesIngredient',
        related_name='recipes',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes',
        verbose_name='Теги'
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
        on_delete=models.PROTECT,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Количество ингредиента'
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('-ingredient',)

    def __str__(self):
        return (f'{self.amount}'
                f' {self.ingredient.measurement_unit}'
                f' {self.ingredient}')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shopping_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='in_shopping_list',
        verbose_name='Список рецептов'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_list_recipe'
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='in_favorite'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'
            ),
        )

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном у {self.user}'
