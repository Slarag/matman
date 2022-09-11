from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff'] # , 'ssh_allowed', 'samba_allowed']
    # inlines = (ProfileInline) , SshPubKeyInline)
    # list_filter = (SshPermFilter, SambaPermFilter, 'is_staff', 'is_superuser', 'is_active', 'groups')
    #
    # def ssh_allowed(self, obj) -> bool:
    #     return obj.has_perm('netaccess_users.can_use_ssh')
    #
    # def samba_allowed(self, obj) -> bool:
    #     return obj.has_perm('netaccess_users.can_use_samba')
    #
    # ssh_allowed.boolean = True
    # samba_allowed.boolean = True


admin.site.unregister(User)
admin.site.register(User, UserAdmin)