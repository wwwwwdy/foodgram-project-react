from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipe.models import Recipe
from .models import CustomUser, Follow


class UserRegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField(max_length=254,
                                   help_text='Введите почту',)
    username = serializers.CharField(max_length=150,
                                     help_text='Введите имя пользователя')
    first_name = serializers.CharField(max_length=150,
                                       help_text='Введите ваше имя')
    last_name = serializers.CharField(max_length=150,
                                      help_text='Введите вашу фамилию')

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        fields = ('username', 'email', 'id',
                  'first_name', 'last_name', 'is_subscribed')
        model = CustomUser

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or not user:
            return False
        return True


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:

        asd = UserSerializer(many=True)

        model = CustomUser
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email')


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "user",)


# class FollowUserSerializer(serializers.ModelSerializer):
#     following = serializers.SerializerMethodField()
#     is_subscribed = serializers.SerializerMethodField()
#
#     class Meta:
#         model = CustomUser
#         fields = ('following', 'is_subscribed',)
#         extra_kwargs = {"password": {"write_only": True}}
#
#     def get_following(self, obj):
#         return FollowersSerializer(obj.following.all(), many=True).data
#
#     def get_is_subscribed(self, obj):
#         user = self.context.get('request').user
#         if user.is_anonymous:
#             return False
#         return True
class FollowUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'following',)
        constraints = [
            UniqueTogetherValidator(queryset=Follow.objects.all(), fields=['user', 'following'])
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return FollowUserSerializer(instance, context=context).data


class RecipeFollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'id', 'cooking_time', 'image',)
        model = Recipe


class FollowUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.ReadOnlyField(source='recipes.count')

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)[:int(recipes_limit)]
        return RecipeFollowSerializer(queryset, many=True).data

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=obj, following=request.user).exists()

