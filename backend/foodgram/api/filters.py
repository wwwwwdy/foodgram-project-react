from django_filters import FilterSet, filters

from recipe.models import Recipe, Favorite



class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug', lookup_expr='contains')
    # is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_favorited = filters.NumberFilter(method='filter_is_favorited')
    # is_favorited = filters.ModelChoiceFilter(queryset=Favorite.objects.filter(user=user))
    class Meta:
        model = Recipe
        fields = ('tags',)

    def filter_is_favorited(self, queryset, name, value):
        if value is True:
            return queryset.filter(favorite__user=self.request.user)
        else:
            return queryset.filter(favorite__user__isnull=True)
