from django.db import models


class Tags(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Название тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет',
        help_text='Цвет для тега'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='slug'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-name',)

    def __str__(self):
        return self.name
