from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
import datetime as dt
from reviews.models import  Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True,
    )
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        required=True,
    )
    class Meta:
        fields = '__all__'
        model = Title
        extra_kwargs = {
            'name': {'required': True, 'max_length': 256},
            'year': {'required': True},
            'genre': {'required': True},
            'category': {'required': True},
        }

    def validate_year(self, value):
        if value > dt.datetime.now().year:
            raise serializers.ValidationError('Вы из будущего?')
        return value
    
    def validate_category(self, value):
        queryset = Category.objects.values_list('slug', flat=True)
        if value not in queryset:
            raise serializers.ValidationError('Нет такой категории!11')
        return value
    
    def validate_genre(self, value):
        queryset = Genre.objects.values_list('slug', flat=True)
        for genre in value:
            if genre not in queryset:
                raise serializers.ValidationError('Нет такого жанра!11')
        return value  


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre
