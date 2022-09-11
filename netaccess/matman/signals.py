from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# from django_auth_ldap.backend import populate_user

from .models import UserProfile


# @receiver(populate_user)
# def handle_ldap_populate_user(sender, user, ldap_user, **kwargs):
#     try:
#         user.profile
#     except UserProfile.DoesNotExist:
#         profile = UserProfile(user=user)
#         profile.save()


@receiver(post_save, sender=User)
def handle_create_user(sender, instance, **kwargs):
    try:
        instance.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=instance)
        profile.save()

