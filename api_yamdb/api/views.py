from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title


class ReviewViewset(viewsets.ModelViewSet):
    """Viewset для объектов модели Review."""
    serializer_class = ReviewSerializer

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Возвращает queryset с отзывами для текущего произведения."""
        return self.get_title().reviews.all().order_by('id')

    def perform_create(self, serializer):
        """Создаёт отзыв для текущего произведения,
        где автором является данный пользователь."""
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели Comment."""
    serializer_class = CommentSerializer

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.all().order_by('id')

    def perform_create(self, serializer):
        """Создает комментарий для текущего отзыва,
        где автором является данный пользователь."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
