from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from taggit.managers import TaggableManager


class Scheme(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    prefix = models.CharField(max_length=10, unique=True)
    numlen = models.PositiveIntegerField(default=6)
    postfix = models.CharField(max_length=10, blank=True, default='')
    is_active = models.BooleanField(default=True)
    _id_counter = models.PositiveBigIntegerField(default=0)

    def get_next_id(self):
        self._id_counter += 1
        self.save()
        return f'{self.prefix}{self._id_counter:0{self.numlen}}{self.postfix}'

    def __str__(self):
        return f'{self.name}'


class Material(models.Model):
    identifier = models.SlugField(unique=True, editable=False)
    serial_number = models.CharField(max_length=30, blank=True)
    material_number = models.CharField(max_length=30, blank=True)
    manufacturer = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='owned_materials', null=True)
    tags = TaggableManager(blank=True)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier.upper()

    def get_absolute_url(self):
        return reverse('material-detail', kwargs={'identifier': self.identifier})

    def get_active_borrow(self):
        try:
            return self.borrows.filter(returned_at__isnull=True).get()
        except ObjectDoesNotExist:
            return None


class Borrow(models.Model):
    item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='borrows')
    borrowed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(blank=True, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    default_scheme = models.ForeignKey(Scheme, blank=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'




