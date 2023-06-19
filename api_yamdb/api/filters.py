from django_filters.filterset import CharFilter, FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    """Фильтр, позволяющий работать с полями ForeignKey."""
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
