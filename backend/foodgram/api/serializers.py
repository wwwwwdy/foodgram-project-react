from rest_framework import serializers
from recipe.models import Tag, Ingredient, Recipe, User
from djoser.serializers import UserSerializer
from djoser.serializers import UserCreateSerializer


class UserRegistrationSerializer(UserCreateSerializer):
    email = serializers.CharField(max_length=254, help_text='Введите почту', )
    username = serializers.CharField(max_length=150, help_text='Введите имя пользователя')
    first_name = serializers.CharField(max_length=150, help_text='Введите ваше имя')
    last_name = serializers.CharField(max_length=150, help_text='Введите вашу фамилию')
    password = serializers.CharField(max_length=150, help_text='Введите пароль')

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password',)


class CustomUserSerializer(UserSerializer):
    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        model = User


class RecipeSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(slug_field='slug', many=True, queryset=Tag.objects.all())
    ingredients = serializers.StringRelatedField(read_only=True, many=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Recipe


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Ingredient
