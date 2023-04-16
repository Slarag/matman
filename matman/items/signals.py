from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
# from django_auth_ldap.backend import populate_user

from . import models

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid='items.UserProfile creation handler')
def create_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        models.UserProfile.objects.create(user=instance)
