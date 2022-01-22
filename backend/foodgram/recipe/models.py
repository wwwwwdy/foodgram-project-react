from colorfield.fields import ColorField
from django.db import models

from users.models import CustomUser


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='Наименование ингридиента')
    measurement_unit = models.CharField(max_length=50,
                                        verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Наименование тэга')
    color = ColorField(max_length=7, default='#FF0000')
    slug = models.SlugField(max_length=200, db_index=True,
                            unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Рецепт')
    name = models.CharField(max_length=200,
                            verbose_name='Наименование рецепта',
                            help_text='Введите наименование')
    image = models.ImageField(upload_to='recipe/',
                              help_text='Загрузите изображение',
                              verbose_name='Изображение')
    text = models.TextField(verbose_name='Описание',
                            help_text='Заполните описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='IngredientRecipe',
                                         verbose_name='ингредиенты')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='тэги')
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   null=True, blank=True)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='unique_recipe')
        ]

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='favorite')

    class Meta:
        verbose_name = 'Избранные рецепты'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(fields=('user', 'recipe'),
                                    name='unique_favorite')
        ]

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name='shoppingcart')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='shopping')
    constraints = [
        models.UniqueConstraint(fields=('user', 'recipe'),
                                name='unique_shoppingcart')
    ]

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} {self.recipe}'
