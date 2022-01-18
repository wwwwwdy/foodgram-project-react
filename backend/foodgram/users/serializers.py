import email
from urllib import request
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
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        fields = ('username', 'email', 'id', 'first_name', 'last_name', 'is_subscribed')
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


class FollowUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ("email", "id", "username", "first_name", "last_name",)
        extra_kwargs = {"password": {"write_only": True}}
#
    def get_following(self, obj):
        return FollowersSerializer(obj.following.all(), many=True).data
    
    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return True
#
#     def get_followers(self, obj):
#         return FollowersSerializer(obj.follower.all(), many=True).data

class SerializerFollow(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='following.id')
    email = serializers.ReadOnlyField(source='following.email')
    username = serializers