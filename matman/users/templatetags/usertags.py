from django import template

from django.conf import settings


register = template.Library()


@register.simple_tag()
def get_registration_allowed():
    return getattr(settings, 'ALLOW_REGISTRATION', False)


@register.simple_tag()
def get_pw_reset_allowed():
    return getattr(settings, 'ALLOW_CHANGE_PASSWORD', False)


@register.simple_tag()
def get_pw_change_allowed():
    return getattr(settings, 'ALLOW_CHANGE_PASSWORD', False)

