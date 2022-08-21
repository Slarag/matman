from django.apps import AppConfig


class NetaccessUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'netaccess_users'

    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals
