from django.contrib.auth.models import AbstractUser
from django.db import models
from reviews.base_models import BaseModel


class Genre(BaseModel):
    slug = models.SlugField(unique=True)


class Category(BaseModel):
    slug = models.SlugField(unique=True)


class CustomUser(AbstractUser):
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


class Title(BaseModel):
    year = models.IntegerField
    rating = models.IntegerField
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
    )
