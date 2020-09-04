from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    '''Роли пользователей'''
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    '''Расширение стандартной модели пользователя Django'''
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=255, 
        choices=UserRole.choices,
        default=UserRole.USER
        )