from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CustomUser, Favorite, Ingredient, Recipe, Tag


class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'username')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="100"')

    get_image.short_description = 'Постер'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Favorite)
