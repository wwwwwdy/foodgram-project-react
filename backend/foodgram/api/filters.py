from django_filters import filters, FilterSet
from recipe.models import Recipe

CHOICES
class RecipeFilter(FilterSet):
    tags = filters.CharFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    print(tags)
    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited')

    def filter_is_favorited(self, queryset, value):
        if value == 1:
            if self.request.user.is_authenticated:
                return queryset.filter(favorite__user=self.request.user)
        else:
            return queryset.filter(favorite_recipe__user__isnull=0)