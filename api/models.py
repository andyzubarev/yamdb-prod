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


class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=250)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True
    )
    description = models.CharField(max_length=2000, null=True, blank=True)
    genre = models.ManyToManyField(Genre,)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )


class Review(models.Model):
    SCORE = (
        (1, 'One Star'),
        (2, 'Two Stars'),
        (3, 'Three Stars'),
        (4, 'Four Stars'),
        (5, 'Five Stars'),
    )
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    created = models.DateTimeField('date published', auto_now_add=True)
    title = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(choices=SCORE)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField('date published', auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text
