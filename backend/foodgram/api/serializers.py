from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField)

from recipe.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                           ShoppingCart, Tag)
from users.serializers import CustomUserSerializer
from .fields import Base64ImageField


class TagSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(ModelSerializer):

    """Сериализатор ингридиентов"""
    class Meta:
        fields = ('name', 'measurement_unit', 'id')
        model = Ingredient


class IngredientRecipeSerializer(ModelSerializer):

    """Сериализатор ингридиентов для создания рецепта"""

    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField()
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('name', 'measurement_unit', 'id', 'amount',)


class RecipeListSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField(use_url=True)
    ingredients = SerializerMethodField(read_only=True)
    is_favorited = SerializerMethodField(read_only=True)
    is_in_shopping_cart = SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'image', 'ingredients',
                  'name', 'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        pass


class RecipeSerializer(ModelSerializer):

    """Сериализатор создания рецепта"""

    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField(use_url=True)
    # is_favorited = SerializerMethodField('get_is_favorited')

    class Meta:
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time', 'author')
        read_only_fields = ('author',)
        model = Recipe

    # def get_is_favorited(self, obj):
    #     user = self.context['request'].user
    #     if user.is_anonymous:
    #         return False
    #     return Favorite.objects.filter(user=user,
    #                                    recipe=obj).exists()

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            )

    def create_tags(self, tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author,
                                       **validated_data)
        self.create_ingredients(ingredients, recipe)
        self.create_tags(tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.create_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data

    # def validate(self, data):
    #     ingredients = data.get("ingredients")
    #     if not ingredients:
    #         raise serializers.ValidationError(
    #             "Рецепту обязательно нужны ингридиенты!"
    #         )
    #     ingredient_list = []
    #     for ingredient_item in ingredients:
    #         ingredient = get_object_or_404(
    #             Ingredient,
    #             id=ingredient_item["id"],
    #         )
    #         if ingredient in ingredient_list:
    #             raise serializers.ValidationError(
    #                 "Пожалуйста, не дублируйте ингридиенты!"
    #             )
    #         ingredient_list.append(ingredient)
    #         if int(ingredient_item["amount"]) < 0:
    #             raise serializers.ValidationError(
    #                 "Количество ингредиента должно быть больше 0!"
    #             )
    #     data["ingredients"] = ingredients
    #     tags = data['tags']
    #     list_tags = []
    #     for tag in tags:
    #         list_tags.append(tag)
    #     if len(list_tags) != len(list(set(list_tags))):
    #         raise serializers.ValidationError(
    #             'Теги не должны повторяться'
    #         )
    #     return data
    # def validate(self, data):
    #     ingredients = data['ingredients']
    #     list_ingredients = []
    #     for ingredient in ingredients:
    #         if ingredient['amount'] <= 0:
    #             raise serializers.ValidationError(
    #                 'Количество ингредиента должно быть больше нуля'
    #             )
    #         list_ingredients.append(ingredient['ingredient'])
    #     if not list_ingredients:
    #         raise serializers.ValidationError(
    #             'Нужно добавить хотя бы один ингредиент'
    #         )
    #     if len(list_ingredients) != len(list(set(list_ingredients))):
    #         raise serializers.ValidationError(
    #             'Ингридиенты не должны повторяться'
    #         )
    #     if data['cooking_time'] <= 0:
    #         raise serializers.ValidationError(
    #             'Время готовки должно быть больше нуля'
    #         )
    #     tags = data['tags']
    #     list_tags = []
    #     for tag in tags:
    #         list_tags.append(tag)
    #     if len(list_tags) != len(list(set(list_tags))):
    #         raise serializers.ValidationError(
    #             'Теги не должны повторяться'
    #         )


class FavoriteSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favorite


class ShoppingCartSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ShoppingCart
