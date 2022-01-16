from django_filters import filters, FilterSet
from recipe.models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited')

    def filter_is_favorited(self, queryset, value):
        if value is True:
            return queryset.filter(fav)