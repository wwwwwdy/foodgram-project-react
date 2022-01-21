from django_filters import FilterSet, filters

from recipe.models import Recipe


class RecipeFilter(FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('tags',)
