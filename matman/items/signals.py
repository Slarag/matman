from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
# from django_auth_ldap.backend import populate_user

from . import models

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid='items.UserProfile creation handler')
def create_profile(sender, instance, created, **kwargs):
    if created and not kwargs.get('raw', False):
        models.UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=models.Item, dispatch_uid='items.Item receiver')
# def item_notifications(sender, instance, created, raw, **kwargs):
#     if created:
#         # Item was newly created
#         pass
#     else:
#         # Item was updated
#         pass
#
#
# @receiver(post_save, sender=models.Comment, dispatch_uid='items.Comment receiver')
# def comment_notifications(sender, instance, created, raw, **kwargs):
#     if created:
#         # Item was newly created
#         pass
#     else:
#         # Item was edited
#         pass
#
#
# # Use pre_save here to be able to get changes
# @receiver(pre_save, sender=models.Borrow, dispatch_uid='items.Borrow receiver')
# def borrow_notifications(sender, instance, created, raw, **kwargs):
#     if created:
#         # Item was newly created
#         pass
#     elif
#     else:
#         # Item was updated
#         pass
