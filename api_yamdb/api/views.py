from reviews.models import Category, Genre, Title
from api.mixins import ListCreateDestroyViewSet
from api.serializers import CategorySerializer, GenreSerializer, TitleSerializer
from rest_framework import viewsets


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
