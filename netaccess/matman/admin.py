from django.contrib import admin

from .models import Material, Department, Borrow

admin.site.register(Department)
admin.site.register(Borrow)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'serial_number', 'material_number', 'manufacturer', 'department',
                    'owner', 'is_active', 'creation_date', 'last_updated']
    list_filter = ['is_active', 'creation_date', 'last_updated']
    search_fields = ['owner__username', 'serial_number', 'material_number', 'manufacturer', 'department', 'tags__all']
    ordering = ('last_updated', 'owner')
