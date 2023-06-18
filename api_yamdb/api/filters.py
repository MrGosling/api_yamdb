from django_filters.filterset import FilterSet, CharFilter
from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')