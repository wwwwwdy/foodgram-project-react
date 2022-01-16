from rest_framework import serializers
from recipe.models import Tag, Ingredient, Recipe, CustomUser, IngredientRecipe
from users.serializers import CustomUserSerializer

class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


# class TagRecipeSerializer(serializers.ModelSerializer):
#
#     """Сериализатор тэгов для создания рецепта """
#
#     id = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())
#     class Meta:
#         fields = ('id')
#         model = TagRecipe


class IngredientSerializer(serializers.ModelSerializer):

    """Сериализатор ингридиентов"""
    class Meta:
        fields = ('name', 'measurement_unit', 'id')
        model = Ingredient


class IngredientRecipeSerializer(serializers.ModelSerializer):

    """Сериализатор ингридиентов для создания рецепта"""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('name', 'measurement_unit', 'id', 'amount',)


class RecipeListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    # ingredients = IngredientRecipeSerializer(many=True, read_only=True)
    ingredients = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart')

    def get_ingredients(self, obj):
        queryset = IngredientRecipe.objects.filter(recipe=obj)
        return IngredientRecipeSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        pass

    def get_is_in_shopping_cart(self, obj):
        pass


class RecipeSerializer(serializers.ModelSerializer):

    """Сериализатор создания рецепта"""

#     tags = TagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'author')
        read_only_fields = ('author',)
        model = Recipe

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            )

        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    # def update(self, instance, validated_data):
    #     author = self.context.get('request').user
    #     ingredients = validated_data.pop('ingredients')
    #
    #     recipe = Recipe.objects.create(author=author, **validated_data)
    #     for ingredient in ingredients:
    #         IngredientRecipe.objects.get_or_create(
    #             recipe=recipe,
    #             amount=ingredient.get('amount'),
    #             ingredient=ingredient.get('id')
    #         )
    #     return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data
