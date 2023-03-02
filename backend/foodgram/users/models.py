from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        # validators=(validate_username,),
        error_messages={'unique': "Такой пользователь уже зарегистрирован."},
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        max_length=150,
        blank=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={'unique': "Такой адрес уже зарегистрирован."},
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=max(len(role) for role, verbose in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=ROLE_USER,
        verbose_name='Ролевая группа'
    )
    confirmation_code = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name='Код подтверждения'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    @property
    def is_admin(self):
        return (
                self.role == self.ROLE_ADMIN
                or self.is_superuser
                or self.is_staff
        )

    def __str__(self):
        return self.username


class Follower(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )

    def __str__(self):
        return f'Подписка {self.user} на {self.author}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]
