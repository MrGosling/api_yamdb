import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CharField, ModelSerializer, Serializer
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from api.validators import (validate_role, validate_username_not_me,
                            validate_username_pattern)
from api.base_serializers import CustomSerializer


class CategorySerializer(CustomSerializer):
    """Сериализатор категорий."""
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(CustomSerializer):
    """Сериализатор жанров."""
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('__all__',)


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор произведений."""
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

    class Meta:
        fields = '__all__'
        model = Title

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


class ReviewSerializer(CustomSerializer):
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
        return validate_role(value)

    def validate_username(self, value):
        return validate_username_pattern(value)


class PartialUserSerializer(ModelSerializer):
    """Сериализатор для управления данными пользователя."""
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        return validate_username_pattern(value)


class UserSignupSerializer(Serializer):
    """Сериализатор для регистрации пользователей."""
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def validate(self, value):
        return validate_username_not_me(value)

    def validate_username(self, value):
        return validate_username_pattern(value)


class UserTokenSerializer(ModelSerializer):
    """Сериализатор для получения токена."""
    username = CharField(required=True)
    confirmation_code = CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username',)
