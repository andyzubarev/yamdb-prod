from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    genre = models.ManyToManyField(Genre,)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )


class Review(models.Model):
    '''Отзывы пользователей на произведения'''
    title = models.ForeignKey(
        Title, 
        on_delete=models.CASCADE, 
        related_name='reviews'
        )
    text = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reviews'
        )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
        )
    pub_date = models.DateTimeField(
        'review pub date', 
        auto_now_add=True, 
        db_index=True)


class Comment(models.Model):
    '''Комментарии к отзывам'''
    review = models.ForeignKey(
        Review, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    text = models.TextField()
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
        )
    pub_date = models.DateTimeField(
        'comment pub date', 
        auto_now_add=True, 
        db_index=True
        )
