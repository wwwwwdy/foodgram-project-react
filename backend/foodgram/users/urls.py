from django.urls import include, path

from .views import UserFollowingViewSet

urlpatterns = [
    path('users/subscriptions/',
         UserFollowingViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/subscribe/',
         UserFollowingViewSet.as_view({'post': 'create'})),
    path('users/<int:id>/subscribe/',
         UserFollowingViewSet.as_view({'delete': 'destroy'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
