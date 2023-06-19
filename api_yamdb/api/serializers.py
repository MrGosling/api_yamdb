import datetime as dt
import re

from api_yamdb.settings import PATTERN
from django.core.exceptions import ValidationError
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CharField, ModelSerializer, Serializer
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
    name = serializers.CharField(max_length=256)
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True,
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug',
        required=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        """Переопределённая функция, изменяющая представления жанров и моделей
        при GET запросе."""
        data = super().to_representation(instance)
        genres_data = GenreSerializer(instance.genre.all(), many=True).data
        category_data = CategorySerializer(instance.category).data
        data['genre'] = genres_data
        data['category'] = category_data
        return data

    def get_rating(self, obj):
        """Функция для вычисляемого поля rating."""
        ratings = Review.objects.filter(title__id=obj.id)
        score = ratings.aggregate(Avg('score'))['score__avg']
        return round(score, 2) if score else None

    def validate_name(self, value):
        """Валидация имени - не более 256 знаков."""
        if len(value) > 256:
            raise serializers.ValidationError('name - не более 256 знаков!11')
        return value

    def validate_year(self, value):
        """Валидация года выпуска - год не позже нынешнего."""
        if value > dt.datetime.now().year:
            raise serializers.ValidationError('Вы из будущего?')
        return value

    def update(self, instance, validated_data):
        """Запрет метода PUT."""
        if self.partial:
            return super().update(instance, validated_data)
        else:
            raise MethodNotAllowed('PUT')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'slug': {'required': True, 'max_length': 50},
        }

    def validate_slug(self, value):
        """Валидация поля slug на соответствие паттерну."""
        pattern = r'^[-a-zA-Z0-9_]+$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Поле slug может содержать буквы латинского алфавита в верхнем'
                'и нижнем регистре, цифры от 0-9,подчеркивание(_), дефис(-)')
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'slug': {'required': True, 'max_length': 50},
        }

    def validate_slug(self, value):
        """Валидация поля slug на соответствие паттерну."""
        pattern = r'^[-a-zA-Z0-9_]+$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Поле slug может содержать буквы латинского алфавита в верхнем'
                'и нижнем регистре, цифры от 0-9,подчеркивание(_), дефис(-)')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов для произведений."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    def validate(self, data):
        title = self.context.get('view').kwargs.get('title_id')
        author = self.context['request'].user
        message = 'Вы уже составили отзыв на данное произведение.'
        if Review.objects.filter(title=title, author=author).exists():
            if self.context['request'].method == "POST":
                raise serializers.ValidationError(message)
            return data
        return data

    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}}


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев на отзывы."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        extra_kwargs = {
            'title': {'required': False},
            'review': {'required': False}
        }


class UserSerializer(ModelSerializer):
    """Сериализатор для данных о пользователе."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_role(self, value):
        if value not in ['user', 'moderator', 'admin']:
            raise ValidationError('Такой роли не существует.')
        return value

    def validate_username(self, value):
        if not re.match(PATTERN, value):
            raise ValidationError('Username не соответствует паттерну.')
        return value


class PartialUserSerializer(ModelSerializer):
    """Сериализатор для управления данными пользователя."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        if not re.match(PATTERN, value):
            raise ValidationError('Username не соответствует паттерну.')
        return value


class UserSignupSerializer(Serializer):
    """Сериализатор для регистрации пользователей."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError('Имя пользователя me запрещено!')
        return data

    def validate_username(self, value):
        if not re.match(PATTERN, value):
            raise ValidationError('Username не соответствует паттерну.')
        return value


class UserTokenSerializer(ModelSerializer):
    """Сериализатор для получения токена."""
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username',)