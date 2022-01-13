from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserFollowingViewSet


router = DefaultRouter()
# router.register('users/me', ProfileUserViewSet, basename='me')
# router.register(r'users/(?P<user_id>\d+)/subscribe', APIFollow, basename='subscribe')
# router.register(r'users/subscriptions', APIFollow, basename='subscriptions')
urlpatterns = [
    path('users/subscriptions/', UserFollowingViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/subscribe/', UserFollowingViewSet.as_view({'post': 'create'})),
    path('users/<int:id>/subscribe/', UserFollowingViewSet.as_view({'delete': 'destroy'})),
    # path('users/<int:user_id>/subscribe/', APIFollow.as_view({'post': 'delete'})),
    # path('users/subscriptions/', APIFollow.as_view({'get': 'list'})),
    path('', include('djoser.urls')),
    # re_path(r'^users/$', CustomUserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),

]
