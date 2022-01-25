from django.urls import include, path

from .views import CreateFollow, UserFollowingViewSet

urlpatterns = [
    path('users/subscriptions/',
         UserFollowingViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<int:id>/subscribe/',
         CreateFollow.as_view(),
         name='subscribe'),
    path('users/<int:id>/subscribe/',
         UserFollowingViewSet.as_view({'delete': 'destroy'}),
         name='subscribe'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
