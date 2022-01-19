from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=50)

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
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Рецепт')
    name = models.CharField(max_length=200, verbose_name='Наименование', help_text='Введите наименование')
    image = models.ImageField(upload_to='recipe/', help_text='Загрузите изображение')
    text = models.TextField(verbose_name='Описание', help_text='Заполните описание')
    # ingredients = models.ManyToManyField(to=Ingredient, through='RecipesIngredients')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe')
#     tags = models.ManyToManyField(Tag, through='TagRecipe')
    tags = models.ManyToManyField(Tag, related_name='tags')
    cooking_time = models.IntegerField()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

# class TagRecipe(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tags')
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.tag} {self.recipe}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True, related_name='favorite')


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='shopping')
