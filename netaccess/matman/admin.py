from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from . import models


admin.site.register(models.Scheme)
admin.site.register(models.Borrow, SimpleHistoryAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.MaterialPicture, SimpleHistoryAdmin)
admin.site.register(models.Comment, SimpleHistoryAdmin)
# admin.site.register(models.MaterialBookmark)


@admin.register(models.Material)
class MaterialAdmin(SimpleHistoryAdmin):
    list_display = ['identifier', 'serial_number', 'material_number', 'manufacturer', 'scheme',
                    'owner', 'is_active', 'creation_date', 'last_updated']
    list_filter = ['is_active', 'creation_date', 'last_updated']
    search_fields = ['owner__username', 'serial_number', 'material_number', 'manufacturer', 'scheme', 'tags__all']
    # fields = ['short_text']
    ordering = ('last_updated', 'owner')
