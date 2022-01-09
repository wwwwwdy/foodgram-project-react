from django.contrib import admin

from .models import Tag, Ingredient, Recipe, CustomUser


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    # На странице рецепта вывести общее число добавлений этого рецепта в избранное.


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Recipe, RecipeAdmin)
# admin.site.unregister(User)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
