from django.contrib.auth.tokens import default_token_generator
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
from reviews.models import Category, CustomUser, Genre, Review, Title

from api.filters import TitleFilter
from api.mixins import ListCreateDestroyViewSet
from api.permissions import (AdminPermission, CustomPermission,
                             TitlesGenresCategoriesPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, PartialUserSerializer,
                             ReviewSerializer, TitleSerializer, UserSerializer,
                             UserSignupSerializer, UserTokenSerializer)
from api.utils import confirm_code_send_mail, get_tokens_for_user


class TitleViewSet(ModelViewSet):
    """Viewset для объектов модели Title."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        TitlesGenresCategoriesPermission
    ]


class GenreViewSet(ListCreateDestroyViewSet):
    """Viewset для объектов модели Genre."""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        TitlesGenresCategoriesPermission
    ]
    filter_backends = (SearchFilter,)
    search_fields = ['name']


class CategoryViewSet(ListCreateDestroyViewSet):
    """Viewset для объектов модели Category."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        TitlesGenresCategoriesPermission
    ]
    filter_backends = (SearchFilter,)
    search_fields = ['name']


class ReviewViewSet(ModelViewSet):
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


class CommentViewSet(ModelViewSet):
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
    """Вьюсет для управления данными пользователей."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = "username"
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = PartialUserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        user = request.user
        serializer = PartialUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthViewSet(ModelViewSet):
    """Вьюсет для регистрации и авторизации пользователей."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny]
    )
    def signup(self, request):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get('username')
        email = request.data.get('email')

        try:
            user, created = CustomUser.objects.get_or_create(
                username=username,
                email=email,
            )
        except IntegrityError:
            return Response(
                "Пользователь с таким именем или почтой уже существует.",
                status=status.HTTP_400_BAD_REQUEST
            )

        confirm_code = default_token_generator.make_token(user)
        confirm_code_send_mail(username, email, confirm_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny]
    )
    def token(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = get_object_or_404(
            CustomUser, username=request.data['username']
        )
        if default_token_generator.check_token(
            user=username, token=request.data['confirmation_code']
        ):
            token_for_user = get_tokens_for_user(user=username)
            return Response(token_for_user, status=status.HTTP_200_OK)
        raise ValidationError('Переданы не корректные данные.')
