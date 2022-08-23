from django.contrib import admin

from .models import Material, Scheme, Borrow, UserProfile

admin.site.register(Scheme)
admin.site.register(Borrow)
admin.site.register(UserProfile)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'serial_number', 'material_number', 'manufacturer', 'scheme',
                    'owner', 'is_active', 'creation_date', 'last_updated']
    list_filter = ['is_active', 'creation_date', 'last_updated']
    search_fields = ['owner__username', 'serial_number', 'material_number', 'manufacturer', 'scheme', 'tags__all']
    ordering = ('last_updated', 'owner')
