from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.utils.timezone import now


from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords, HistoricForeignKey


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Scheme(models.Model):
    # Model fields
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    prefix = models.CharField(max_length=10, blank=True, default='')
    numlen = models.PositiveIntegerField(default=6)
    postfix = models.CharField(max_length=10, blank=True, default='')
    is_active = models.BooleanField(default=True)

    # Internal fields
    _id_counter = models.PositiveBigIntegerField(default=0)

    # # Model managers
    # active = ActiveManager()
    # objects = models.Manager()

    def get_next_id(self) -> str:
        """
        Get the next valid ID from the scheme.

        Internal ID counter of the scheme will be incremented in an atomic operation to avoid possible duplicates.
        :return: New, unused ID from scheme.
        """

        with transaction.atomic():
            self._id_counter += 1
            self.save()
        return f'{self.prefix}{self._id_counter:0{self.numlen}}{self.postfix}'

    def __str__(self):
        return f'{self.name}'

    def clean(self, *args, **kwargs):
        if not any((self.prefix, self.postfix)):
            raise ValidationError('At least either prefix or postfix must be specified')
        try:
            if self != Scheme.objects.get(prefix=self.prefix, postfix=self.postfix):
                raise ValidationError('Combination of prefix and postfix must be unique')
        except Scheme.DoesNotExist:
            pass
        except Scheme.MultipleObjectsReturned as exc:
            raise ValidationError('Combination of prefix and postfix must be unique')
        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('edit-scheme', kwargs={'pk': self.id})


class Material(models.Model):
    # Model fields
    identifier = models.SlugField(unique=True, editable=False)
    short_text = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=30, blank=True)
    revision = models.CharField(max_length=30, blank=True)
    material_number = models.CharField(max_length=30, blank=True)
    manufacturer = models.CharField(max_length=30, blank=True)
    description = models.TextField(blank=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=100, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='owned_materials', null=True)
    tags = TaggableManager(blank=True)
    is_active = models.BooleanField(default=True)
    contains = models.ManyToManyField('self', related_name='contained_in', symmetrical=False, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    # # Model managers
    # active = ActiveManager()
    # objects = models.Manager()

    def __str__(self):
        return self.identifier.upper()

    def save(self, *args, **kwargs):
        if self.identifier == '':
            self.identifier = self.scheme.get_next_id()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('material-detail', kwargs={'identifier': self.identifier})

    def get_active_borrow(self):
        try:
            return self.borrows.filter(returned_at__isnull=True).get()
        except ObjectDoesNotExist:
            return None

    def is_bookmarked_by_user(self, user) -> bool:
        return user.profile.bookmarks.filter(pk=self.pk).exists()


class MaterialPicture(models.Model):
    # Model fields
    material = HistoricForeignKey(Material, related_name='pictures', on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=100, blank=True)
    file = models.ImageField(upload_to='pictures/')
    history = HistoricalRecords()

    @property
    def absolute_image_url(self):
        return f'{settings.MEDIA_URL}{self.file.url}'


class Borrow(models.Model):
    # Model fields
    item = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='borrows')
    borrowed_at = models.DateTimeField(auto_now_add=True)
    borrowed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='borrows')
    notes = models.TextField(blank=True)
    usage_location = models.CharField(max_length=100, blank=True, null=False)
    estimated_returndate = models.DateField(blank=True, null=True)
    returned_at = models.DateTimeField(blank=True, null=True)
    returned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                    related_name='borrows_returned')
    history = HistoricalRecords()

    def close(self, returned_by, returned_at=None):
        if returned_at is None:
            returned_at = now()
        self.returned_by = returned_by
        self.returned_at = returned_at
        self.save()

    def get_absolute_url(self):
        return reverse('borrow-edit', kwargs={'pk': self.pk})


class UserProfile(models.Model):
    # Model fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    default_scheme = models.ForeignKey(Scheme, blank=True, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    initials = models.CharField(max_length=10, null=True, blank=True, unique=True)
    about = models.TextField(blank=True)

    bookmarks = models.ManyToManyField(Material, related_name='bookmarked_by')

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def clean(self):
        self.initials = self.initials.lower()

    def has_bookmarked(self, material: Material):
        return self.bookmarks.filter(pk=material.pk).exists()

    def bookmark(self, material: Material):
        self.bookmarks.add(material)

    def unbookmark(self, material: Material):
        self.bookmarks.remove(material)


class Comment(models.Model):
    # Model fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    creation_date = models.DateTimeField(auto_now_add=True)
    # last_updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    material = models.ForeignKey(Material, related_name='comments', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'Comment by {self.author.username} on {self.material}'

    def get_absolute_url(self):
        return reverse('comment-edit', kwargs={'pk': self.pk})


# # ToDo:
# class MaterialBookmark(models.Model):
#     # Model fields
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
#     material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='bookmarks')
