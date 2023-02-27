from django.contrib.auth.models import AbstractUser
from django.db import models


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
        #validators=(validate_username,),
        error_messages={'unique': "Такой пользователь уже зарегистрирован."},
        verbose_name='Имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        blank=False
    )
    last_name = models.CharField(
        max_length=150,
        blank = False
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
