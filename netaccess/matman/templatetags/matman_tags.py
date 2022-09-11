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


# @register.simple_tag
# def materials_owned(user):
#     return Material.objects.filter(owner=user)
#
#
# @register.simple_tag
# def materials_borrowed(user):
#     return Material.objects.filter(borrows__borrowed_by=user, borrows__returned_at__isnull=True)
#
# @register.simple_tag
# def materials_borrowed_fromme(user):
#     return Material.objects.exclude(borrows=None).filter(owner=user, borrows__returned_at__isnull=True)

@register.simple_tag(takes_context=True)
def get_params(context):
    get = context['request'].GET
    if not get:
        return ''
    return get.urlencode() + '&'
