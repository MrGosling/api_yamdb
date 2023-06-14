from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime as dt
from reviews.models import  Category, Genre, Title, Review
from django.db.models import Avg
from rest_framework.exceptions import MethodNotAllowed


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
