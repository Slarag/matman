import datetime

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db.models import Q


from .models import SshPubKey, PermitOpenRestriction


class PermitOpenAdmin(admin.TabularInline):
    model = PermitOpenRestriction
    list_display = [' hostname', 'port']
    extra = 1


class ExpiryFilter(admin.SimpleListFilter):
    title = 'key expired'
    parameter_name = 'expired'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Expired'),
            ('false', 'Not expired'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'true':
            return queryset.filter(expiration_date__lte=datetime.datetime.now().date())
        elif value == 'false':
            return queryset.exclude(expiration_date__lte=datetime.datetime.now().date())
        return queryset


class PermFilterBase(admin.SimpleListFilter):
    title: str = ''
    parameter_name: str = ''
    perm = None

    def lookups(self, request, model_admin):
        return (
            ('true', 'Yes'),
            ('false', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'true':
            return queryset.filter(Q(groups__permissions=self.perm) | Q(user_permissions=self.perm) | Q(is_superuser=True))
        elif value == 'false':
            return queryset.exclude(Q(groups__permissions=self.perm) | Q(user_permissions=self.perm) | Q(is_superuser=True))
        return queryset


class SshPermFilter(PermFilterBase):
    title = 'SSH allowed'
    parameter_name = 'ssh_allowed'
    perm = Permission.objects.get(codename='can_use_ssh')


class SambaPermFilter(PermFilterBase):
    title = 'Samba allowed'
    parameter_name = 'samba_allowed'
    perm = Permission.objects.get(codename='can_use_samba')


class RestrictedFilter(admin.SimpleListFilter):
    title = 'key restricted'
    parameter_name = 'restricted'

    def lookups(self, request, model_admin):
        return (
            ('true', 'Restricted'),
            ('false', 'Unrestricted'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'true':
            return queryset.exclude(permit_open=None)
        elif value == 'false':
            return queryset.filter(permit_open=None)
        return queryset


# @admin.display(description='Username')
# def username(obj):
#     return obj.user.username


class SshPubKeyHelper:
    def is_active(self, obj) -> bool:
        return not obj.is_expired

    def is_unrestricted(self, obj) -> bool:
        return not obj.permit_open.all()

    is_active.boolean = True
    is_unrestricted.boolean = True


@admin.register(SshPubKey)
class SshPubKeyAdmin(SshPubKeyHelper, admin.ModelAdmin):
    list_display = ['name', 'user', 'comment', 'is_active', 'is_unrestricted', 'expiration_date', 'date_added', 'last_updated']
    list_filter = ['date_added', 'last_updated', 'expiration_date', ExpiryFilter, RestrictedFilter]
    search_fields = ['user__username', 'comment']
    ordering = ('last_updated', 'user')
    raw_id_fields = ('user',)
    inlines = [PermitOpenAdmin]
    # extra = 0


class SshPubKeyInline(SshPubKeyHelper, admin.TabularInline):
    model = SshPubKey
    can_delete = True
    ordering = ('last_updated', 'user')
    fields = ('name', 'comment', 'expiration_date', 'is_active', 'is_unrestricted')
    show_change_link = True
    readonly_fields = ('name', 'comment', 'expiration_date', 'is_active', 'is_unrestricted')
    inlines = [PermitOpenAdmin]
    extra = 0


