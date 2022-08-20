from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=64)

    def __str__(self):
        return f'Profile for user {self.user.username}'
    