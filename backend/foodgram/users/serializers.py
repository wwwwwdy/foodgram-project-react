from djoser.serializers import UserCreateSerializer, TokenSerializer, UserSerializer
from rest_framework import serializers
from .models import CustomUser, Follow
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

class UserRegistrationSerializer(UserCreateSerializer):
    email = serializers.EmailField(max_length=254, help_text='Введите почту',)
    username = serializers.CharField(max_length=150, help_text='Введите имя пользователя')
    first_name = serializers.CharField(max_length=150, help_text='Введите ваше имя')
    last_name = serializers.CharField(max_length=150, help_text='Введите вашу фамилию')
    # password = serializers.CharField(max_length=150, help_text='Введите пароль')

    class Meta(UserCreateSerializer.Meta):
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'password')


class UserTokenSerializer(TokenSerializer):
    pass


class CustomUserSerializer(UserSerializer):
    # username = serializers.CharField(max_length=150)
    # email = serializers.CharField(max_length=254)
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    is_subscribed = serializers.BooleanField(default=False)

    class Meta:
        fields = ('username', 'email', 'id', 'first_name', 'last_name', 'is_subscribed')
        model = CustomUser


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True, source='author.id')
    email = serializers.EmailField(read_only=True, source='author.email')
    username = serializers.CharField(read_only=True, source='author.username')
    first_name = serializers.CharField(read_only=True, source='author.first_name')
    last_name = serializers.CharField(read_only=True, source='author.last_name')

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
# class FollowSerializer(serializers.ModelSerializer):
#     user = SlugRelatedField(
#         read_only=True,
#         slug_field='username',
#         default=serializers.CurrentUserDefault()
#     )
#     following = SlugRelatedField(
#         slug_field='username', queryset=CustomUser.objects.all()
#     )
#
#     class Meta:
#         fields = '__all__'
#         model = Follow
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=('user', 'following'),
#             )
#         ]

    def validate_following(self, value):
        if self.context['request'].user == value:
            raise serializers.ValidationError('Вы уже подписаны ')
        return value
