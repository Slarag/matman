from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .. import models
from .. import forms
from .mixins import ActiveMixin


class SchemeListView(ActiveMixin, ListView):
    model = models.Scheme
    template_name_suffix = '_list'
    fields = ['name', 'prefix', 'numlen', 'postfix', 'is_active']
    active_context = 'schemes'

    def get_paginate_by(self, queryset):
        return self.request.GET.get('items', 10)

    def get_ordering(self):
        orderby = self.request.GET.get('orderby', 'name')
        direction = self.request.GET.get('direction', 'asc')
        if direction not in ['asc', 'desc']:
            direction = 'asc'
        if direction == 'desc':
            orderby = f'-{orderby}'
        return orderby

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        context['fields'] = self.fields
        context['orderby'] = self.request.GET.get('orderby', 'name')
        context['direction'] = self.request.GET.get('direction', 'asc')
        return context


class SchemeCreateView(ActiveMixin, PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Scheme
    template_name_suffix = '_create'
    form_class = forms.scheme.SchemeCreateForm
    success_url = reverse_lazy('list-schemes')
    active_context = 'schemes'
    permission_required = 'schemes.add'

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully created scheme <a href="{url}" class="alert-link">{self.object}</a>'


class SchemeEditView(ActiveMixin, PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Scheme
    template_name_suffix = '_edit'
    form_class = forms.scheme.SchemeEditForm
    success_url = reverse_lazy('list-schemes')
    active_context = 'schemes'
    permission_required = 'schemes.change'

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully updated scheme <a href="{url}" class="alert-link">{self.object}</a>'
