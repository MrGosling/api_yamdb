from rest_framework import serializers
from reviews.models import Comment, Review
from rest_framework.serializers import ModelSerializer, EmailField, CharField
from django.core.exceptions import ValidationError
import re
from reviews.models import CustomUser
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime as dt
from reviews.models import Category, Genre, Title, Review
from django.db.models import Avg
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.validators import UniqueTogetherValidator


class TitleSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'year': {'required': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        genres_data = GenreSerializer(instance.genre.all(), many=True).data
        category_data = CategorySerializer(instance.category).data
        data['genre'] = genres_data
        data['category'] = category_data
        return data

    def get_rating(self, obj):
        ratings = Review.objects.filter(title__id=obj.id)
        score = ratings.aggregate(Avg('score'))['score__avg']
        return round(score, 2) if score else None

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError('Вы из будущего?')
        return value
    
    def update(self, instance, validated_data):
        if self.partial:
            return super().update(instance, validated_data)
        else:
            raise MethodNotAllowed('PUT')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'slug': {'required': True, 'max_length': 50},
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'slug': {'required': True, 'max_length': 50},
        }


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
    # username = CharField(required=False, max_length=150)
    # email = EmailField(required=True, max_length=254)
    # first_name = CharField(required=False, max_length=150)
    # last_name = CharField(required=False, max_length=150)
    # bio = CharField(required=False)
    # role = CharField(required=False)

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
        pattern = (r'^[\w.@+-]+$')

        if not re.match(pattern, value):
            raise ValidationError('Username не соответствует паттерну.')
        return value


class PartialUserSerializer(ModelSerializer):
    # username = CharField(required=False, max_length=150)
    # email = EmailField(required=False, max_length=254)
    # first_name = CharField(required=False, max_length=150)
    # last_name = CharField(required=False, max_length=150)
    # bio = CharField(required=False)
    # role = CharField(read_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)

    def validate_username(self, value):
        pattern = (r'^[\w.@+-]+$')

        if not re.match(pattern, value):
            raise ValidationError('Username не соответствует паттерну.')
        return value


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError('Имя пользователя me запрещено!')
        return data

    def validate_username(self, value):
        pattern = (r'^[\w.@+-]+$')

        if not re.match(pattern, value):
            raise ValidationError('Username не соответствует паттерну.')
        return value


class UserTokenSerializer(ModelSerializer):
    username = CharField(required=False)
    confirmation_code = CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
        read_only_fields = ('username',)
