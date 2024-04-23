import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Фильтр для модели Title."""

    name = django_filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    genre = django_filters.CharFilter(field_name='genre__slug')
    category = django_filters.CharFilter(field_name='category__slug')
    year = django_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ('genre__slug', 'category__slug', 'name', 'year')
