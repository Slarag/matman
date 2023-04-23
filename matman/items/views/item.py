import csv
import re
from collections import namedtuple
import urllib
import traceback
import functools
import io

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, get_user
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.db import transaction
from django.core.exceptions import ValidationError

from .. import models
from .. import forms
from .. import filters
from .mixins import ActiveMixin, ViewFormsetHelperMixin
from .. import tasks

User = get_user_model()

CronObject = namedtuple('CronObject', ['timestamp', 'type', 'object'])


class ItemCreateView(ActiveMixin, ViewFormsetHelperMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Item
    template_name_suffix = '_create'
    form_class = forms.item.ItemCreateForm
    formset_class = forms.pictures.PictureFormset
    formset_helper = forms.pictures.PictureFormSetHelper
    active_context = 'add'

    def get_reference(self):
        try:
            reference_id = self.request.GET.get('reference')
            reference = models.Item.objects.get(identifier=reference_id)
        except (ObjectDoesNotExist, KeyError):
            return None
        else:
            return reference

    def get_initial(self):
        initial = super().get_initial().copy()
        initial['owner'] = self.request.user
        initial['scheme'] = self.request.user.profile.default_scheme

        reference = self.get_reference()
        if reference:
            values = model_to_dict(reference, fields=self.get_form_class().Meta.fields)
            initial.update(values)
            initial['reference'] = reference.identifier

        return initial

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully created item <a href="{url}" class="alert-link">{self.object}</a>'

    def get_success_url(self):
        if 'add_other' in self.request.POST:
            return reverse_lazy('add-item') + '?' + urllib.parse.urlencode({'reference': self.object.identifier})
        return super().get_success_url()

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(instance=form.instance)

        reference = self.get_reference()
        if reference:
            formset = self.formset_class(instance=reference)
            formset.instance = form.instance

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # Get reference directly from POST data as I need this info even if the form might be invalid
        refid = self.request.POST.get('reference', None)
        reference = None
        if refid:
            reference = self.model.objects.get(identifier=refid)
        formset = self.formset_class(self.request.POST, self.request.FILES, instance=reference)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)

        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()

        if formset.instance:
            # reference was used
            for ff in formset:
                if ff.empty_permitted and not ff.has_changed():
                    continue
                ff.instance.item = self.object
                ff.instance.pk = None
                ff.instance.save()
        else:
            formset.instance = form.instance
            formset.save()

        tasks.send_item_notifications.delay(self.object.pk, created=True,
                                            editor_pk=self.request.user.pk if self.request.user else None)
        return super().form_valid(form)

    def form_invalid(self, form, formset):
        messages.error(self.request, 'An error occurred while updating the item')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


# Important: No login required for details
class ItemDetailView(ActiveMixin, DetailView):
    model = models.Item
    template_name_suffix = '_detail'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
    form_class = forms.comment.CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cb = [CronObject(x.creation_date, 'comment', x) for x in self.object.comments.all().order_by('-creation_date')]
        # Last 5 borrows
        cb += [CronObject(x.borrowed_at, 'borrow', x) for x in self.object.borrows.all().order_by('-borrowed_at')[:5]]
        cb.sort(key=lambda x: x.timestamp)
        context['comments_borrows'] = cb
        context['comment_form'] = self.kwargs.get('comment_form', forms.comment.CommentForm())
        context['is_bookmarked'] = False
        if self.request.user.is_authenticated:
            context['is_bookmarked'] = self.object.is_bookmarked_by_user(self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form = self.form_class(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.item = self.object
            comment.author = request.user
            comment.save()
            url = self.object.get_absolute_url()
            messages.success(
                self.request,
                f'Successfully created comment on item <a href="{url}" class="alert-link">{self.object}</a>'
            )
            tasks.send_comment_notifications.delay(comment.pk, created=True,
                                                   editor_pk=self.request.user.pk if self.request.user else None)
            return self.render_to_response(self.get_context_data())

        messages.error(self.request, 'Error while creating comment')
        return self.render_to_response(
            self.get_context_data(comment_form=form)
        )


class ItemEditView(ActiveMixin, ViewFormsetHelperMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Item
    template_name_suffix = '_edit'
    form_class = forms.item.ItemEditForm
    formset_class = forms.pictures.PictureFormset
    formset_helper = forms.pictures.PictureFormSetHelper
    related_name = 'pictures'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully updated item <a href="{url}" class="alert-link">{self.object}</a>'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(instance=form.instance)

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(self.request.POST, self.request.FILES, instance=form.instance)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)

        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.save()
        tasks.send_item_notifications.delay(self.object.pk, created=False,
                                            editor_pk=self.request.user.pk if self.request.user else None)

        return super().form_valid(form)

    def form_invalid(self, form, formset):
        messages.error(self.request, 'An error occurred while updating the item')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


# https://gist.github.com/MikaelSantilio/3e761b325c7fd7588207cec06fdcbefb
class FilteredListView(ListView):
    filterset_class = None
    allow_empty = True

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context


class ItemListView(ActiveMixin, FilteredListView):
    model = models.Item
    fields = ['serial_number', 'part_number', 'manufacturer', 'scheme', 'owner', 'tags', 'is_active']
    filterset_class = filters.ItemFilter
    template_name_suffix = '_list'
    active_context = 'search'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('items', 10)

    def get_ordering(self):
        direction = self.request.GET.get('direction', 'asc')
        if direction not in ['asc', 'desc']:
            direction = 'asc'

        orderby = self.request.GET.get(f'orderby', 'identifier')
        if direction == 'desc':
            orderby = f'-{orderby}'
        return orderby

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bookmarked'] = []
        if self.request.user.is_authenticated:
            context['bookmarked'] = self.request.user.profile.bookmarks.all()

        direction = self.request.GET.get('direction', 'asc')
        if direction not in ['asc', 'desc']:
            direction = 'asc'
        orderby = self.request.GET.get(f'orderby', 'identifier')
        # context['items'] = self.get_paginate_by(self.queryset)
        context['direction'] = direction
        context['orderby'] = orderby
        return context


class ItemCsvImportView(LoginRequiredMixin, FormView):
    form_class = forms.item.ItemCsvImportForm
    template_name = 'items/item_csv_import.html'
    csv_fieldnames = [
        'identifier',
        'short_text',
        'serial_number',
        'revision',
        'part_number',
        'manufacturer',
        'description',
        'location',
        'owner',
        'is_active',
        'tags'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csv_fieldnames'] = self.csv_fieldnames
        return context

    def __init__(self):
        super().__init__()
        self._csv_cleaning_funcs = {}
        clean_func_prefix = 'csv_clean_'
        for x in dir(self):
            if x.startswith(clean_func_prefix):
                fieldname = x[len(clean_func_prefix):]
                func = getattr(self, x)
                if callable(func):
                    self._csv_cleaning_funcs[fieldname] = func
        self.form = None
        self.identifier_pattern = None
        self.max_encountered = 0

    def get_initial(self):
        initial = super().get_initial()
        initial['scheme'] = self.request.user.profile.default_scheme
        return initial

    def csv_clean_tags(self, value: str) -> list[str]:
        """
        Split list of tags by according delimiter. Ignore blanks.
        :param tags: string which is a list of tags
        :return: list of tags (strings)
        """

        delimiter = self.form.cleaned_data['tag_delimiter']
        return [s.strip() for s in value.split(delimiter) if s.strip() != '']

    def csv_clean_is_active(self, value: str) -> bool:
        """
        Convert value to bool. This function is case-insensitive and evaluates True for "yes", "true", "1".
        :param value:
        """
        return value.lower() in ['yes', 'true', '1']

    @functools.lru_cache()
    def csv_clean_owner(self, value: str) -> User:
        return User.objects.get(username=value)

    def csv_clean_identifier(self, value: str) -> str:
        match = self.identifier_pattern.fullmatch(value)
        min_number = self.form.cleaned_data['scheme']._id_counter
        if not match:
            raise ValueError(f'Invalid identifier: {value}')
        number = int(match.group('number'))
        if number <= min_number:
            raise ValueError(f'Cannot assign identifier {value} (Number must be greater than {min_number}')
        if number > self.max_encountered:
            self.max_encountered = number
        return value

    def csv_clean(self, linedata: dict[str, str]) -> dict[str]:
        cleaned = {}
        for fieldname, value in linedata.items():
            # Ignore blank values
            if not value:
                continue
            cleaning_funcname = f'csv_clean_{fieldname}'
            if hasattr(self, cleaning_funcname):
                cleaned[fieldname] = getattr(self, cleaning_funcname)(value.strip())
            else:
                cleaned[fieldname] = value.strip()

        return cleaned

    def form_valid(self, form):
        self.form = form
        scheme = form.cleaned_data['scheme']
        new_items = []
        file = io.TextIOWrapper(self.request.FILES['file'].file)


        scheme = self.form.cleaned_data['scheme']
        self.identifier_pattern = re.compile(fr'{scheme.prefix}(?P<number>\d{{{scheme.numlen}}}){scheme.postfix}')

        # with open(file, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(file, delimiter=form.cleaned_data['delimiter'])

        for name in reader.fieldnames:
            if name not in self.csv_fieldnames:
                messages.error(self.request, f'Invalid field name: {name}')
                return super().render_to_response(context=self.get_context_data())

        for lineno, data in enumerate(reader, start=1):
            try:
                data = self.csv_clean(data)

                data['scheme'] = scheme

                # owner
                if form.cleaned_data['set_owner'] and 'owner' not in data:
                    data['owner'] = self.request.user

                print(data)

                tags = data.pop('tags', [])
                item = models.Item(**data)
                item.full_clean()
                new_items.append((item, tags))
            except (ValidationError, ValueError, KeyError) as exc:
                # exc.lineno = lineno
                messages.error(self.request, f'Error in line {lineno}: {traceback.format_exception_only(exc)[0]}')
                return super().render_to_response(context=self.get_context_data())

        try:
            # with transaction.atomic():
            # Update scheme from database in case new items were created by other users while parsing csv
            scheme = models.Scheme.objects.get(pk=scheme.pk)
            original_count = scheme._id_counter
            if scheme._id_counter < self.max_encountered:
                scheme._id_counter = self.max_encountered
            scheme.save()
            scheme = models.Scheme.objects.get(pk=scheme.pk)
            print(scheme._id_counter)
            # Sort new items in way that items with an already given identifier appear first to avoid conflicts while saving
            new_items.sort(key=lambda x: (x[0].identifier == '', x[0].identifier))
            for item, tags in new_items:
                print(repr(item))
                print(repr(item.identifier))
                item.save()
                item.tags.set(tags)
        except Exception as exc:
            messages.error(self.request, f'Unexpected error while saving items: {traceback.format_exception_only(exc)[0]}')
            for item, tags in new_items:
                if item.id is not None:
                    # Item was saved and needs to be deleted
                    item.delete()
            scheme._id_counter = original_count
            scheme.save()
        else:
            messages.success(self.request, f'Successfully imported {len(new_items)} items')

        return super().render_to_response(context=self.get_context_data())
