import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import reverse


class SshPubKey(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pubkeys')
    pubkey = models.CharField(max_length=1024)
    comment = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    expiration_date = models.DateField(blank=True, null=True)

    @property
    def is_expired(self) -> bool:
        if self.expiration_date is None:
            return False
        return self.expiration_date <= datetime.datetime.now().date()

    def __str__(self):
        return f'SSH Public Key "{self.name}"'

    def to_authorized_keys_line(self) -> str:
        s = ''
        if self.permit_open.all():
            s += ''.join(f'permit-open={x}' for x in self.permit_open.all())
        if self.expiration_date is not None:
            if s:
                s += ','
            s += f'expiry-time={self.expiration_date.strftime("%Y%m%d")}'
        s += f' {self.pubkey}'
        return s

    def get_absolute_url(self):
        return reverse('key-detail', args=[str(self.id)])


class PermitOpenRestriction(models.Model):
    pubkey = models.ForeignKey(SshPubKey, on_delete=models.CASCADE, related_name='permit_open')
    hostname = models.CharField(max_length=100)
    port = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.hostname}:{"*" if self.port is None else self.port}'


class SystemPermissions(models.Model):
    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ('can_use_ssh', 'Allow SSH access'),
            ('can_use_samba', 'Allow Samba access'),
        )
