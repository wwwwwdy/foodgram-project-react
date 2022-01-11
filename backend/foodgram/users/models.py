from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
# User = get_user_model()


class CustomUser(AbstractUser):
    is_subscribed = models.BooleanField(default=False)
    REQUIRED_FIELDS = ('first_name', 'last_name', 'email')


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower')
    # following = models.ForeignKey(
    #     CustomUser, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'following'),
                                    name='unique_list')
        ]

    def __str__(self):
        f"{self.user} follows {self.following}"
