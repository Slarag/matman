from django.conf import settings


def user_settings_context(request):
    return {
        'allow_registration': bool(getattr(settings, 'ALLOW_REGISTRATION', False)),
        'allow_change_pw': bool(getattr(settings, 'ALLOW_CHANGE_PASSWORD', False)),
        'allow_reset_pw': bool(getattr(settings, 'ALLOW_RESET_PASSWORD', False)),
    }

