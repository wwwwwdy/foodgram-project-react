from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TagViewSet, RecipeViewSet, IngredientViewSet, FavoriteViewSet, ShoppingCartView


router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
# router.register(r'recipes/<int:recipe_id>/favorite/', FavoriteViewSet, basename='favorite')
urlpatterns = [
    # path('recipes/favorites/', FavoriteViewSet.as_view({'post': 'create'})),
    path('recipes/<int:recipe_id>/favorite/', FavoriteViewSet.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
    path('', include(router.urls)),
]
