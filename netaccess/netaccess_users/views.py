import datetime

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .models import SshPubKey


@login_required
def dashboard(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard',
                   'ssh_keys_total': request.user.pubkeys.all().count(),
                   'ssh_keys_active': request.user.pubkeys.exclude(expiration_date__gt=datetime.datetime.now().date()).count()
                   })


@login_required
def keys_view(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'keys'})


@login_required
def edit_view(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard'})


@login_required
def dhcp_overview(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard'})


@login_required
def dhcp_overview(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard'})


class SshPubKeyListView(LoginRequiredMixin, ListView):
    model = SshPubKey
    paginate_by = 20
    # template_name = 'netaccess_users/sshpubkey_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'keys'
        return context

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class KeyDetailView(LoginRequiredMixin, DetailView):
    model = SshPubKey
    fields = ['name', 'comment', 'expiration_date', 'pubkey']
    template_name_suffix = '_detail'


class KeyEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SshPubKey
    fields = ['name', 'comment', 'expiration_date', 'pubkey']
    template_name_suffix = '_update'
    success_message = "%(name)s was updated successfully"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_ajax'] = self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        return context


class KeyDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SshPubKey
    template_name_suffix = '_delete'
    success_message = "SSH key was deleted successfully"
    success_url = reverse_lazy('key-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_ajax'] = self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
        return context


class KeyCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SshPubKey
    template_name_suffix = '_create'
    success_message = "SSH key was added successfully"
    success_url = reverse_lazy('key-list')
    fields = ['name', 'comment', 'expiration_date', 'pubkey']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
