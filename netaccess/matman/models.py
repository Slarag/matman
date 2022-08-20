from django.db import models
from django.conf import settings
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    id_prefix = models.CharField(max_length=3)
    _id_counter = models.PositiveBigIntegerField(default=0)

    def get_next_id(self):
        self._id_counter += 1
        self.save()
        return f'{self.id_prefix}{self._id_counter:06}'

    def __str__(self):
        return f'{self.name}'


class Location(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=2000)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='storage_locs_owned', null=True)

    def __str__(self):
        return f'{self.name}'


class Material(models.Model):
    identifier = models.SlugField(unique=True, editable=False)
    serial_number = models.CharField(max_length=30, blank=True)
    material_number = models.CharField(max_length=30, blank=True)
    manufacturer = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='owned_materials', null=True)
    is_active = models.BooleanField(default=True)
    # tags = ...

    def __str__(self):
        return self.identifier.upper()

    def get_absolute_url(self):
        return reverse('material-detail', kwargs={'identifier': self.identifier})


class Borrow(models.Model):
    item = models.ForeignKey(Material, on_delete=models.CASCADE)
    borrowed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    returned_at = models.DateTimeField(blank=True)


