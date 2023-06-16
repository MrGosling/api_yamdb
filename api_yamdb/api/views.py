from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from api.permissions import AdminPermission, UserPermission, CustomPermission, CategoriesGenresPermission, TitlesPermission
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Category, Genre, Title, Review, Title, CustomUser
from api.mixins import ListCreateDestroyViewSet
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, CommentSerializer,
                             ReviewSerializer, UserSerializer,
                             PartialUserSerializer)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, TitlesPermission]


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CategoriesGenresPermission]


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CategoriesGenresPermission]


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset для объектов модели Review."""
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermission]
    pagination_class = PageNumberPagination

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
    permission_classes = [CustomPermission]
    pagination_class = PageNumberPagination

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


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    lookup_field = "username"

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[UserPermission]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = PartialUserSerializer(request.user)
            return Response(serializer.data)

        user = request.user
        serializer = PartialUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
