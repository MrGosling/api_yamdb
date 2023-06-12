from django.db import models
from reviews.base_models import BaseModel


class Genre(BaseModel):
    # name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Category(BaseModel):
    # name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(BaseModel):
    # name = models.CharField(max_length=200)
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
