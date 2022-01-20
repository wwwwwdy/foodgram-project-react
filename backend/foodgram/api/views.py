from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from recipe.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                           ShoppingCart, Tag)

from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
from .utils import render_to_pdf


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tags',)


class APIDownload(APIView):
    def get(self, request):
        pdf = render_to_pdf('shopping_cart.html')
        return HttpResponse(pdf, content_type="application/pdf")
