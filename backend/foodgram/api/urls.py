from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework.authtoken import views
from .views import TagViewSet, RecipeViewSet, IngredientViewSet, CustomUserViewSet, Logout
from djoser import urls
router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.obtain_auth_token),
    path('auth/token/logout/', Logout.as_view()),
]