from django.contrib import admin
from users.models import Follow
# Register your models here.+


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


admin.site.register(Follow, FollowAdmin)