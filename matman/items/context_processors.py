from django.conf import settings


def external_resources(request):
    if hasattr(settings, 'EXTERNAL_RESOURCES'):
        return {'resources': settings.EXTERNAL_RESOURCES}
