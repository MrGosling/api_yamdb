from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.base_models import BaseModel


class CustomUser(AbstractUser):
    """Кастомная модель пользователей"""
    ROLE_TYPE = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    ]

    bio = models.TextField(
        'Биография',
        null=True,
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        choices=ROLE_TYPE,
        default='user',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username'],
                name='unique_username'
            ),
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'
            )
        ]

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_superuser


class Genre(BaseModel):
    slug = models.SlugField(max_length=50, unique=True)


class Category(BaseModel):
    slug = models.SlugField(max_length=50, unique=True)


class Title(BaseModel):
    year = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
    )


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='genres',
        on_delete=models.SET_NULL,
        null=True,
    )
    genre = models.ForeignKey(
        Title,
        related_name='titles',
        on_delete=models.SET_NULL,
        null=True,
    )


class Review(models.Model):
    """Модель отзывов на произведения, а так же их рейтинг"""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    text = models.TextField(
        null=False,
        verbose_name='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Разрешены значения от 1 до 10'),
            MaxValueValidator(10, 'Разрешены значения от 1 до 10'),
        ]
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']


class Comment(models.Model):
    """Модель комментариев к отзыву произведений."""
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст комментария',)
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Отзыв',
    )

    class Meta:
        ordering = ['-pub_date']
