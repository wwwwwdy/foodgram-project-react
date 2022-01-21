from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from recipe.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                           ShoppingCart, Tag)

from .filters import RecipeFilter
from .mixins import AddingAndDeletingListMixin
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tags',)

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeSerializer
        return RecipeListSerializer


class FavoriteViewSet(AddingAndDeletingListMixin, APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = FavoriteSerializer
    model_class = Favorite
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tags',)


class ShoppingCartView(AddingAndDeletingListMixin, APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShoppingCartSerializer
    model_class = ShoppingCart
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('tags',)
    filterset_class = RecipeFilter


class APIDownload(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        recipes = request.user.shoppingcart.all().values_list(
            'recipe', flat=True)
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__in=recipes).annotate(sum=(Sum('amount')))
        )
        buying_list = {}
        for ingredient in ingredients:
            name = ingredient.ingredient.name
            amount = ingredient.amount
            unit = ingredient.ingredient.measurement_unit
            if name not in buying_list:
                buying_list[name] = {'amount': amount, 'unit': unit}
            else:
                buying_list[name]['amount'] = (
                    buying_list[name]['amount'] + amount
                )
        shopping_list = []
        for item in buying_list:
            shopping_list.append(
                f'{item} - {buying_list[item]["amount"]}, '
                f'{buying_list[item]["measurement_unit"]}\n'
            )
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = (
            'attachment;' 'filename="shopping_list.txt"'
        )
        return response
