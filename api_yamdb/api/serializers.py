from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime as dt
from reviews.models import  Category, Genre, Title, Review
from django.db.models import Avg


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
            'genre': {'required': True},
            'category': {'required': True},
        }

    def get_rating(self, obj):
        ratings = Review.objects.filter(title__id=obj.id)
        score = ratings.aggregate(Avg('score'))['score__avg']
        return round(score, 2) if score else None

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError('Вы из будущего?')
        return value
    
    # def validate_category(self, value):
    #     queryset = list(Category.objects.all())
    #     # queryset = Category.objects.values_list('slug', flat=True)
    #     if value not in queryset:
    #         raise serializers.ValidationError('Нет такой категории!11')
    #     return value
    
    # def validate_genre(self, value):
    #     # queryset = Genre.objects.all()
    #     print(value)
    #     queryset = list(Genre.objects.values_list('slug', flat=True))
    #     print(queryset)
    #     for genre in value:
    #         print(type(genre))
    #         if genre not in queryset:
    #             raise serializers.ValidationError('Нет такого жанра!11')
    #     # if value not in queryset:
    #     #     raise serializers.ValidationError('Нет такой жанра!11')
    #     return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
