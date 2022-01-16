from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TagViewSet, RecipeViewSet, IngredientViewSet, APIFavorite


router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes/<int:id>/favorite', APIFavorite)
urlpatterns = [
    # path('recipes/<int:id>/favorite/', APIFavorite.as_view()),
    path('', include(router.urls)),
]
