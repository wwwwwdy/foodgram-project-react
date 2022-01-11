from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from .views import APIFollowers, APIFollow


router = DefaultRouter()
# router.register('users/me', ProfileUserViewSet, basename='me')
# router.register(r'users/(?P<user_id>\d+)/subscribe', APIFollow, basename='subscribe')
# router.register(r'users/subscriptions', APIFollow, basename='subscriptions')
urlpatterns = [
    path('users/<int:user_id>/subscribe/', APIFollow.as_view({'post': 'delete'})),
    path('users/subscriptions/', APIFollow.as_view({'get': 'list'})),
    path('', include('djoser.urls')),
    # re_path(r'^users/$', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),

]
