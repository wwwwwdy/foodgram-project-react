from rest_framework.routers import DefaultRouter
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from .views import TagViewSet, RecipeViewSet, IngredientViewSet
router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]