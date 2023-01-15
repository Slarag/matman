from collections import namedtuple
import datetime
import urllib

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchQuery, SearchRank
from django.forms.models import model_to_dict

from .. import models
from .. import forms


CronObject = namedtuple('CronObject', ['timestamp', 'type', 'object'])


class MaterialListView(ListView):
    model = models.Material
    fields = ['serial_number', 'material_number', 'manufacturer', 'scheme', 'owner', 'tags', 'is_active']
    paginate_by = 20

    def get_ordering(self):
        ordering = self.request.GET.get('orderby', '-identifier')
        return ordering

    def get_template_names(self):
        if self.request.GET.get('view', 'list') == 'cards':
            self.template_name_suffix = '_list_cards'
        else:
            self.template_name_suffix = '_list'
        return super().get_template_names()


class MaterialCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Material
    template_name_suffix = '_create'
    form_class = forms.material.MaterialForm
    formset_class = forms.pictures.PictureFormset
    formset_helper = forms.pictures.PictureFormSetHelper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset_helper'] = self.formset_helper()
        return context

    def get_reference(self):
        try:
            reference_id = self.request.GET.get('reference')
            reference = models.Material.objects.get(identifier=reference_id)
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
        return f'Successfully created material <a href="{url}" class="alert-link">{self.object}</a>'

    def get_success_url(self):
        if 'add_other' in self.request.POST:
            return reverse_lazy('add-material') + '?' + urllib.parse.urlencode({'reference': self.object.identifier})
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
                ff.instance.material = self.object
                ff.instance.pk = None
                ff.instance.save()
        else:
            formset.instance = form.instance
            formset.save()

        return super().form_valid(form)

    def form_invalid(self, form, formset):
        messages.error(self.request, 'An error occurred while updating the material')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


# Important: No login required for details
class MaterialDetailView(DetailView):
    model = models.Material
    template_name_suffix = '_detail'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
    form_class = forms.comment.CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cb = [CronObject(x.creation_date, 'comment', x) for x in self.object.comments.all().order_by('-creation_date')]
        cb += [CronObject(x.borrowed_at, 'borrow', x) for x in self.object.borrows.all().order_by('-borrowed_at')]
        cb.sort(key=lambda x: x.timestamp)
        context['comments_borrows'] = cb
        context['comment_form'] = self.kwargs.get('comment_form', forms.comment.CommentForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form = self.form_class(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.material = self.object
            comment.author = request.user
            comment.save()
            url = self.object.get_absolute_url()
            messages.success(
                self.request,
                f'Successfully created commend on material <a href="{url}" class="alert-link">{self.object}</a>'
            )
            return self.render_to_response(self.get_context_data())

        messages.error(self.request, 'Error while creating comment')
        return self.render_to_response(
            self.get_context_data(comment_form=form)
        )


class MaterialEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Material
    template_name_suffix = '_edit'
    form_class = forms.material.MaterialEditForm
    formset_class = forms.pictures.PictureFormset
    formset_helper = forms.pictures.PictureFormSetHelper
    related_name = 'pictures'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully updated material <a href="{url}" class="alert-link">{self.object}</a>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset_helper'] = self.formset_helper()
        return context

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
        messages.error(self.request, 'An error occurred while updating the material')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


def search(request):
    form = forms.material.SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = forms.material.SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                material = models.Material.objects.get(identifier=query)
                return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
            except ObjectDoesNotExist:
                pass
            search_vector = SearchVector('identifier', 'short_text', 'serial_number', 'material_number',
                                         'manufacturer', 'description', 'location', 'tags__name')
            search_query = SearchQuery(query, search_type='websearch')
            search_rank = SearchRank(search_vector, search_query)
            results = models.Material.objects.annotate(rank=search_rank).order_by('-rank').distinct()
    return render(request,
                  'matman/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
