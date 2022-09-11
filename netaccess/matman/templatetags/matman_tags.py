from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
import markdown

from ..models import Material, Borrow

register = template.Library()


@register.filter(name='markdown')
@stringfilter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag(takes_context=True)
def get_params(context):
    get = context['request'].GET
    if not get:
        return ''
    return get.urlencode() + '&'


@register.filter()
def alert_class(level_tag):
    mapping = {
        'debug': 'alert-secondary',
        'info': 'alert-primary',
        'success': 'alert-success',
        'warning': 'alert-warning',
        'error': 'alert-danger',
    }
    return mapping[level_tag]


@register.filter()
def alert_icon(level_tag):
    mapping = {
        'debug':   '#info-fill',
        'info':    '#info-fill',
        'success': '#check-circle-fill',
        'warning': '#exclamation-triangle-fill',
        'error':   '#exclamation-triangle-fill',
    }
    return mapping[level_tag]