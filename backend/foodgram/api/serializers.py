from rest_framework import serializers
from recipe.models import Tag, Ingredient, Recipe, CustomUser, IngredientRecipe, Favorite, ShoppingCart
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
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        pass


class RecipeSerializer(serializers.ModelSerializer):

    """Сериализатор создания рецепта"""

#     tags = TagSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    ingredients = IngredientRecipeSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
# 	is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'author')
        read_only_fields = ('author',)
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()
#
# 	def get_is_in_shopping_cart(self, obj):
# 		user = self.context['request'].user
# 		if user.is_anonymous:
# 			return False
# 		return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

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

    def update(self, instance, validated_data):
        author = self.context.get('request').user
        instance.ingredients.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        instance.tags.clear()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=instance,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            )
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.save()

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeListSerializer(instance, context=context).data

    def validate(self, data):
        ingredients = data['ingredients']
        list_ingredients = []
        for ingredient in ingredients:
            if ingredient['amount'] <= 0:
                raise serializers.ValidationError(
                    'Количество ингредиента должно быть больше нуля'
                )
            list_ingredients.append(ingredient['ingredient'])
        if not list_ingredients:
            raise serializers.ValidationError(
                'Нужно добавить хотя бы один ингредиент'
            )
        if len(list_ingredients) != len(list(set(list_ingredients))):
            raise serializers.ValidationError(
                'Ингридиенты не должны повторяться'
            )
        if data['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Время готовки должно быть больше нуля'
            )
        tags = data['tags']
        list_tags = []
        for tag in tags:
            list_tags.append(tag)
        if len(list_tags) != len(list(set(list_tags))):
            raise serializers.ValidationError(
                'Теги не должны повторяться'
            )
        return data


class FavoriteSerializer(serializers.ModelSerializer):

    # image = Base64ImageField(use_url=True)
    # recipe = RecipeListSerializer()
    class Meta:
        fields = '__all__'
        # read_only_fields = ('id', 'name', 'image', 'cooking_time')
        model = Favorite


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = ShoppingCart
