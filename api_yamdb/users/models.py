from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель Пользователя."""

    class Role(models.TextChoices):
        USER = 'user', _('User')
        ADMIN = 'admin', _('Admin')
        MODERATOR = 'moderator', _('Moderator')

    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(
        unique=True, blank=False, null=False, max_length=254
    )
    role = models.CharField(
        max_length=30, choices=Role.choices, default='user'
    )
    bio = models.TextField(blank=True)
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff

    @property
    def is_moderator(self):
        return self.is_authenticated and self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
