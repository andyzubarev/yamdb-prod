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


class Title(models.Model):
    pass


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


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
