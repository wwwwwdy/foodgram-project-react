from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import ProfileUserViewSet, FollowViewSet


router = DefaultRouter()
# router.register('users/me', ProfileUserViewSet, basename='me')
router.register(r'users/(?P<user_id>\d+)/subscribe', FollowViewSet, basename='subscribe')
router.register(r'users/subscriptions', FollowViewSet, basename='subscriptions')
urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    # re_path(r'^users/$', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('auth/', include('djoser.urls.authtoken')),
]
