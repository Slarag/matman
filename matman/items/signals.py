from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
# from django_auth_ldap.backend import populate_user

from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        UserProfile.objects.create(user=instance)

