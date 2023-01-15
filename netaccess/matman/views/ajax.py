from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from taggit.models import Tag


@require_GET
def tag_suggestions(request):
    value = request.GET.get('value', '')
    tags = Tag.objects.filter(name__startswith=value).order_by('name')[:100]
    return JsonResponse({'suggestions': [tag.name for tag in tags]})
