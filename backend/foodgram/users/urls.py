from django.urls import include, path

from .views import UserFollowingViewSet, SubscriptionsView

urlpatterns = [
    path('users/subscriptions/',
         UserFollowingViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('users/<int:id>/subscribe/',
         UserFollowingViewSet.as_view({'post': 'create'}),
         name='subscribe'),
    path('users/<int:id>/subscribe/',
         UserFollowingViewSet.as_view({'delete': 'destroy'}),
         name='subscribe'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
