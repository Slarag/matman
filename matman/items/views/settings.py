from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .. import models
from .. import forms
from .mixins import ActiveMixin


class SettingsView(ActiveMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.UserProfile
    form_class = forms.settings.SettingsForm
    template_name_suffix = '_edit'
    success_message = 'Profile settings updated successfully'
    active_context = 'settings'

    def get_success_url(self):
        return reverse_lazy('profile-settings')

    def get_object(self, queryset=None):
        return self.request.user.profile


class AboutView(ActiveMixin, TemplateView):
    template_name = "about.html"
    active_context = 'about'
