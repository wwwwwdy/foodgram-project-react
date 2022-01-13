from djoser.serializers import UserCreateSerializer, TokenSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser, Follow
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField
from recipe.models import Recipe

class UserRegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField(max_length=254, help_text='Введите почту',)
    username = serializers.CharField(max_length=150, help_text='Введите имя пользователя')
    first_name = serializers.CharField(max_length=150, help_text='Введите ваше имя')
    last_name = serializers.CharField(max_length=150, help_text='Введите вашу фамилию')
    # password = serializers.CharField(max_length=150, help_text='Введите пароль')

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('username', 'email', 'id', 'first_name', 'last_name', 'is_subscribed')
        model = CustomUser


class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:

        asd = UserSerializer(many=True)

        model = CustomUser
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email')


class FollowingSerializer(serializers.ModelSerializer):

#     following = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "user",)


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("email", "id", "username", "first_name", "last_name",)
        extra_kwargs = {"password": {"write_only": True}}
#
    def get_following(self, obj):
        return FollowersSerializer(obj.following.all(), many=True).data
#
#     def get_followers(self, obj):
#         return FollowersSerializer(obj.follower.all(), many=True).data
