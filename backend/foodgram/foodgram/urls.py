from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('api/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

]
