from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
# User = get_user_model()


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    # is_subscribed = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'following'),
                                    name='unique_list')
        ]

    def __str__(self):
        return f"{self.user} follows {self.following}"
