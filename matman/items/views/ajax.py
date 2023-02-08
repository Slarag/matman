import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from taggit.models import Tag
from ..models import Item


@require_GET
def tag_suggestions(request):
    value = request.GET.get('value', '')
    tags = Tag.objects.filter(name__istartswith=value).order_by('name')[:100]
    return JsonResponse({'suggestions': [tag.name for tag in tags]})


@require_GET
def user_suggestions(request):
    value = request.GET.get('value', '')
    users = User.objects.filter(username__istartswith=value).order_by('username')[:100]
    return JsonResponse({'suggestions': [users.username for users in users]})


@login_required
@require_POST
def toggle_bookmark(request):
    identifier = json.loads(request.body).get('identifier', '')
    item = get_object_or_404(Item, identifier=identifier)
    profile = request.user.profile
    if profile.has_bookmarked(item):
        profile.unbookmark(item)
    else:
        profile.bookmark(item)
    return JsonResponse({'item': item.identifier, 'bookmarked': profile.has_bookmarked(item)})
