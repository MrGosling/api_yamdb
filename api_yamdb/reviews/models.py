from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    """Модель отзывов на произведения, а так же их рейтинг"""
    author = models.ForeignKey(
        # CustomUser,
        on_delete=models.CASCADE,
        related_name='rewiews',
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
        # Title,
        on_delete=models.CASCADE,
        related_name='rewiews',
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
        return f"{self.id}"

    class Meta:
        ordering = ['-pub_date']


class Comment(models.Model):
    """Модель комментариев к отзыву произведений."""
    author = models.ForeignKey(
        # CustomUser,
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
