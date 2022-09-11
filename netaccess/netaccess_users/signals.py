from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from django.conf import settings

# https://docs.djangoproject.com/en/4.0/ref/signals/#post-save


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def handle_user_changed(sender, instance, created, **kwargs):
    # ToDo
    if created:
        # User was created, create linux and samba accounts
        print(f'CREATE SAMBA FOR {str(instance).upper()}'.center(80, '+'))
    if instance.has_perm('netaccess_user.can_use_samba'):
        # enable samba account
        print(f'ENABLE SAMBA FOR {str(instance).upper()}'.center(80, '+'))
    else:
        # disable samba account
        print(f'DISABLE SAMBA FOR {str(instance).upper()}'.center(80, '+'))

