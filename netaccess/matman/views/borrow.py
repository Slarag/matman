import datetime

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.timezone import now

from .. import models
from .. import forms


class BorrowCreateView(SuccessMessageMixin, CreateView):
    model = models.Borrow
    form_class = forms.borrow.BorrowForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial().copy()
        initial['estimated_returndate'] = (now() + datetime.timedelta(days=7)).date()
        if self.request.user.is_authenticated:
            initial['borrowed_by'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['material'] = get_object_or_404(models.Material, identifier=self.kwargs['identifier'])
        return context

    def get_success_message(self, cleaned_data):
        material = self.get_context_data()['material']
        url = material.get_absolute_url()
        return f'Borrowed material <a href="{url}" class="alert-link">{material}</a>'

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.item.identifier})

    def form_valid(self, form):
        form.instance.item = self.get_context_data()['material']
        return super().form_valid(form)


class BorrowEditView(SuccessMessageMixin, UpdateView):
    model = models.Borrow
    form_class = forms.borrow.BorrowEditForm
    template_name_suffix = '_edit'
    success_message = 'Borrow successfully updated'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.returned_at is not None:
            messages.error(request, 'Cannot edit Borrow as its already closed!')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.item.identifier})


class BorrowCloseView(SuccessMessageMixin, UpdateView):
    model = models.Borrow
    form_class = forms.borrow.BorrowCloseForm
    template_name_suffix = '_close'
    success_message = 'Borrow successfully closed'

    def get_initial(self):
        initial = super().get_initial().copy()
        if self.request.user.is_authenticated:
            initial['returned_by'] = self.request.user
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.returned_at is not None:
            messages.error(request, 'Borrow is already closed!')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = self.object.item
        return context

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.item.identifier})

    def form_valid(self, form):
        if 'close' in self.request.POST:
            self.object.returned_at = now()
            self.object.save()
            material = self.object.item
            messages.success(self.request, f'You have returned {material}')
        return redirect(reverse_lazy('material-detail',
                                     kwargs={'identifier': self.get_context_data()['material'].identifier}))