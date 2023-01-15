from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .. import models
from .. import forms


class SettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.UserProfile
    form_class = forms.settings.SettingsForm
    template_name_suffix = '_edit'
    success_message = 'Profile settings updated successfully'

    def get_success_url(self):
        return reverse_lazy('profile-settings')

    def get_object(self, queryset=None):
        return self.request.user.profile
