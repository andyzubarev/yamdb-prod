from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Avg


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
    rating = models.IntegerField(null=True, blank=True)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка', choices=[(r, r) for r in range(1, 11)],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата оценки', auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.score_avg = Review.objects.filter(title_id=self.title).aggregate(
            Avg('score')
        )
        self.title.rating = self.score_avg['score__avg']
        self.title.save()


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
