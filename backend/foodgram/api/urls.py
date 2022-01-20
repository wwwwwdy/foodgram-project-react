from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, IngredientViewSet, RecipeViewSet, ShoppingCartView, TagViewSet, APIDownload)

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/', FavoriteViewSet.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
    path('recipes/download_shopping_cart/', APIDownload.as_view()),
    path('', include(router.urls)),
]
