from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework import status, filters

from api.permissions import AdminPermission
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Category, Genre, Title, Review, Title, CustomUser
from api.mixins import ListCreateDestroyViewSet
from api.serializers import CategorySerializer, GenreSerializer, TitleSerializer, CommentSerializer, ReviewSerializer, UserSerializer, PartialUserSerializer, UserSignupSerializer, UserTokenSerializer
from api.utils import confirm_code_send_mail, get_tokens_for_user
from django.contrib.auth.tokens import default_token_generator
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
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
