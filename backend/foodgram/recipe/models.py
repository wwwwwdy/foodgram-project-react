from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class User(AbstractUser):
    email = models.CharField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    units = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(max_length=7, default='#FF0000')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='URL')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Рецепт')
    name = models.CharField(max_length=200, verbose_name='Наименование', help_text='Введите наименование')
    image = models.ImageField(upload_to='recipe/', help_text='Загрузите изображение')
    description = models.TextField(verbose_name='Описание', help_text='Заполните описание')
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'



# class MyUserManager(BaseUserManager):
#     def _create_user(self, email, username, first_name, last_name, password, **extra_fields):
#         if not email:
#             raise ValueError('Вы не ввели почту')
#         if not username:
#             raise ValueError('Вы не ввели логин')
#         if not first_name:
#             raise ValueError('Вы не ввели имя')
#         if not last_name:
#             raise ValueError('Вы не ввели фамилию')
#         user = self.model(email=self.normalize_email(email), username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, username, first_name, last_name, password):
#         return self._create_user(email, username, first_name, last_name, password)
#
#     def create_superuser(self, email, username, first_name, last_name, password):
#         return self._create_user(email, username, first_name, last_name, password, is_staff=True, is_superuser=True)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(max_length=254, unique=True)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     objects = MyUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     def __str__(self):
#         return self.username
