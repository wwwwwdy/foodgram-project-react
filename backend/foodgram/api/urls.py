from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APIDownload, FavoriteViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingCartView, TagViewSet)

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view(), name='favorite'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartView.as_view(), name='shopping-cart'),
    path('recipes/download_shopping_cart/',
         APIDownload.as_view(), name='download-shopping-cart'),
    path('', include(router.urls)),
]
