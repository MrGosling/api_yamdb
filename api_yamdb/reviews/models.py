from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_TYPE = ['user', 'moderator', 'admin']


class User(AbstractUser):
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
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]
