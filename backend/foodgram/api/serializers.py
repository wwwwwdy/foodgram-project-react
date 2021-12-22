from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.relations import StringRelatedField
from recipe.models import Tag, Ingredient, Recipe

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer
    ingredients = IngredientSerializer

    class Meta:
        fields = '__all__'
        model = Recipe


class RecipeSerializerCreate(serializers.ModelSerializer):
    # tag = serializers.SlugRelatedField(slug_field='slug', queryset=Tag.objects.all())
    tag = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=Tag.objects.all())

    class Meta:
        fields = '__all__'
        model = Recipe
