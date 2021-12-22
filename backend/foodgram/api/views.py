from rest_framework import viewsets
from djoser.views import UserViewSet
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, UserSerializer
from recipe.models import Tag, Recipe, Ingredient


class CustomUserViewSet(UserViewSet):
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer