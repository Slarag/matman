from typing import Any
from urllib.parse import urlencode

from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
import markdown

register = template.Library()


@register.filter(name='markdown')
@stringfilter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.simple_tag(takes_context=True)
def update_params(context, parameter: str, value: Any):
    query = context['request'].GET.copy()
    query[parameter] = str(value)
    return mark_safe(urlencode(list(query.items())))


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
        'debug':   '#symbol-info-fill',
        'info':    '#symbol-info-fill',
        'success': '#symbol-check-circle-fill',
        'warning': '#symbol-exclamation-triangle-fill',
        'error':   '#symbol-exclamation-triangle-fill',
    }
    return mapping[level_tag]


@register.inclusion_tag('mde_script.html')
def init_mde(css_id):
    return {'css_id': css_id}
