from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

from . import models


admin.site.register(models.Scheme)
admin.site.register(models.Borrow, SimpleHistoryAdmin)
# admin.site.register(models.UserProfile)
admin.site.register(models.MaterialPicture, SimpleHistoryAdmin)
admin.site.register(models.Comment, SimpleHistoryAdmin)
# admin.site.register(models.MaterialBookmark)


@admin.register(models.Material)
class MaterialAdmin(SimpleHistoryAdmin):
    list_display = ['identifier', 'serial_number', 'part_number', 'manufacturer', 'scheme',
                    'owner', 'is_active', 'creation_date', 'last_updated']
    list_filter = ['is_active', 'creation_date', 'last_updated']
    search_fields = ['owner__username', 'serial_number', 'part_number', 'manufacturer', 'scheme', 'tags__all']
    # fields = ['short_text']
    ordering = ('last_updated', 'owner')


class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    max_num = 1
    can_delete = False


class UserAdmin(AuthUserAdmin):
    inlines = [UserProfileInline]


# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)