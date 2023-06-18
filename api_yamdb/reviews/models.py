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

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
    )
    role = models.CharField(
        'Роль',
        max_length=10,
        blank=False,
        choices=ROLE_TYPE,
        default='user',
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        "Имя",
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_superuser

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_superuser


class Genre(BaseModel):
    """Модель жанров."""
    slug = models.SlugField(max_length=50, unique=True)


class Category(BaseModel):
    """Модель категорий."""
    slug = models.SlugField(max_length=50, unique=True)


class Title(BaseModel):
    """Модель произведений и её привязка к жанрам и категориям."""
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
