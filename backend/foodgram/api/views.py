from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipe.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                           ShoppingCart, Tag)

from .filters import RecipeFilter
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


class AddingAndDeletingListMixin:
    serializer_class = None
    model_class = None

    def post(self, request, recipe_id):
        user = self.request.user.id
        data = {"user": user, "recipe": recipe_id}
        serializer = self.serializer_class(
            data=data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        obj = get_object_or_404(
            self.model_class, user=user, recipe__id=recipe_id
        )
        obj.delete()
        model_title = self.model_class._meta.verbose_name.title()
        return Response(
            f"Успешно удалено: {model_title}!", status.HTTP_204_NO_CONTENT
        )


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
            IngredientRecipe.objects.filter(recipe__in=recipes)
            .all()
            .values_list('ingredient', flat=True)
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
