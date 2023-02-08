from collections import namedtuple
import urllib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict

from .. import models
from .. import forms
from .. import filters
from .mixins import ActiveMixin, ViewFormsetHelperMixin

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

        return super().form_valid(form)

    def form_invalid(self, form, formset):
        messages.error(self.request, 'An error occurred while updating the item')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


# https://gist.github.com/MikaelSantilio/3e761b325c7fd7588207cec06fdcbefb
class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
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
