from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .models import Material


class MaterialAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name_suffix = '_create'
    fields = ['serial_number', 'material_number', 'manufacturer', 'description', 'department', 'owner', 'is_active']

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = super().get_initial().copy()
        initial['owner'] = self.request.user.pk
        # initial['department'] = self.request.user.department
        return initial

    def get_success_message(self, cleaned_data):
        return f'Successfully created {self.object}'

    def get_success_url(self):
        if 'add_other' in self.request.POST:
            return reverse_lazy('add-material')
        return super().get_success_url()
        # return reverse_lazy('dashboard')

    def form_valid(self, form):
        department = form.instance.department
        form.instance.identifier = department.get_next_id()
        return super().form_valid(form)


# Important: No login required for details
class MaterialDetailView(DetailView):
    model = Material
    template_name_suffix = '_detail'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'


class MaterialEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name_suffix = '_edit'
    fields = ['serial_number', 'material_number', 'manufacturer', 'description', 'department', 'owner', 'is_active']
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'

    def get_success_message(self, cleaned_data):
        return f'Successfully updated {self.object}'

    def get_success_url(self):
        return self.object.get_absolute_url()
