from rest_framework import serializers
from recipe.models import Tag, Ingredient, Recipe, CustomUser
from users.serializers import CustomUserSerializer
# class RecipesIngredientsSerializer(serializers.ModelSerializer):
#     amount = serializers.IntegerField(max_digits=10, decimal_places=1)
#     id = serializers.PrimaryKeyRelatedField()
#
#     class Meta:
#         model = RecipesIngredients
#         fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        exclude = ('id',)
        model = Recipe

