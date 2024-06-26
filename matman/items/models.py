from __future__ import annotations

from datetime import date

from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager
from simple_history.models import HistoricalRecords, HistoricForeignKey


User = get_user_model()


class ActiveSchemeManager(models.Manager):
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
    history = HistoricalRecords(excluded_fields=['_id_counter'])

    # Internal fields
    _id_counter = models.PositiveBigIntegerField(default=0)

    # # Model managers
    objects = models.Manager()
    active = ActiveSchemeManager()

    def get_next_id(self) -> str | None:
        """
        Get the next valid ID from the scheme.

        Internal ID counter of the scheme will be incremented in an atomic operation to avoid possible duplicates.
        :return: New, unused ID from scheme or None if scheme is not active.
        """

        if not self.is_active:
            return None

        with transaction.atomic():
            # Reload Scheme from DB to ensure _id_counter is up to date
            self.refresh_from_db()
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


class Item(models.Model):
    # Model fields
    identifier = models.SlugField('ID', unique=True, editable=False)
    short_text = models.CharField('Short Text', max_length=100, blank=True)
    serial_number = models.CharField('Serial Number', max_length=30, blank=True)
    revision = models.CharField('Revision/Version', max_length=30, blank=True)
    part_number = models.CharField('Part Number', max_length=30, blank=True)
    manufacturer = models.CharField('Manufacturer', max_length=30, blank=True)
    description = models.TextField('Description', blank=True)
    scheme = models.ForeignKey(Scheme, on_delete=models.SET_NULL, null=True)
    location = models.CharField('Location', max_length=100, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Owner', on_delete=models.SET_NULL,
                              related_name='owned_items', null=True, blank=True)
    tags = TaggableManager('Tags', blank=True)
    is_active = models.BooleanField('Active', default=True)
    # contains = models.ManyToManyField('self', related_name='contained_in', symmetrical=False, blank=True)
    creation_date = models.DateTimeField('Creation Date', auto_now_add=True)
    last_updated = models.DateTimeField('Last edited', auto_now=True)
    history = HistoricalRecords()

    # # Model managers
    # active = ActiveManager()
    # objects = models.Manager()


    def __str__(self):
        return self.identifier.upper()

    def save(self, *args, **kwargs):
        if self._state.adding and self.identifier == '':
            self.identifier = self.scheme.get_next_id()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={'identifier': self.identifier})

    @property
    def active_borrow(self) -> Borrow | None:
        try:
            return self.borrows.filter(returned_at__isnull=True).get()
        except ObjectDoesNotExist:
            return None

    def is_bookmarked_by_user(self, user) -> bool:
        return user.profile.bookmarks.filter(pk=self.pk).exists()


    @property
    def is_borrowed(self) -> bool:
        """
        :return: True if item is currently borrowed, else None
        """
        return self.active_borrow is not None


class ItemPicture(models.Model):
    # Model fields
    item = HistoricForeignKey(Item, verbose_name='Item', related_name='pictures',
                              on_delete=models.CASCADE, blank=True)
    title = models.CharField('Title', max_length=30, blank=True)
    description = models.CharField('Description', max_length=100, blank=True)
    file = models.ImageField(upload_to='pictures/', verbose_name='File')
    history = HistoricalRecords()

    @property
    def absolute_image_url(self):
        return f'{settings.MEDIA_URL}{self.file.url}'


class ActiveBorrowsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(returned_at__isnull=True)


class Borrow(models.Model):
    # Model fields
    item = models.ForeignKey(Item, verbose_name='Item', on_delete=models.CASCADE, related_name='borrows')
    borrowed_at = models.DateTimeField('Borrowed at', auto_now_add=True)
    borrowed_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Borrowed by',
                                    on_delete=models.SET_NULL, null=True, related_name='borrows')
    notes = models.TextField('Notes', blank=True)
    usage_location = models.CharField('Usage Location', max_length=100, blank=True, null=False)
    estimated_returndate = models.DateField('Estimated return date', blank=True, null=True)
    returned_at = models.DateTimeField('Returned at', blank=True, null=True)
    returned_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Returned by', on_delete=models.SET_NULL,
                                    null=True, related_name='borrows_returned')
    history = HistoricalRecords()

    objects = models.Manager()
    active = ActiveBorrowsManager()

    def close(self, returned_by, returned_at=None):
        if returned_at is None:
            returned_at = now()
        self.returned_by = returned_by
        self.returned_at = returned_at
        self.save()

    def get_absolute_url(self):
        return reverse('borrow-edit', kwargs={'pk': self.pk})

    @property
    def due_since(self) -> int:
        """
        Number of day since the estimated_returndate.
        If the return date is in the future, a negative number will be returned.
        """
        today = now().date
        days = (self.estimated_returndate - today).days
        return days

    @property
    def is_closed(self) -> bool:
        return self.returned_at is not None


class UserProfile(models.Model):
    # Model fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    default_scheme = models.ForeignKey(Scheme, blank=True, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=30, blank=True)
    about = models.TextField(blank=True)

    bookmarks = models.ManyToManyField(Item, related_name='bookmarked_by', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    def has_bookmarked(self, item: Item):
        return self.bookmarks.filter(pk=item.pk).exists()

    def bookmark(self, item: Item):
        self.bookmarks.add(item)

    def unbookmark(self, item: Item):
        self.bookmarks.remove(item)


class Comment(models.Model):
    # Model fields
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    creation_date = models.DateTimeField(auto_now_add=True)
    # last_updated = models.DateTimeField(auto_now=True)
    text = models.TextField()
    item = models.ForeignKey(Item, related_name='comments', on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f'Comment by {self.author.username} on {self.item}'

    def get_absolute_url(self):
        return reverse('comment-edit', kwargs={'pk': self.pk})
