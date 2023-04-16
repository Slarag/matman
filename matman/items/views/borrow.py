import datetime

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.timezone import now

from .. import models
from .. import forms


class QuickBorrowView(SuccessMessageMixin, CreateView):
    model = models.Borrow
    form_class = forms.borrow.QuickBorrowForm
    template_name_suffix = '_quick'

    def get_initial(self):
        initial = super().get_initial().copy()
        initial['estimated_returndate'] = (now() + datetime.timedelta(days=7)).date()
        if self.request.user.is_authenticated:
            initial['borrowed_by'] = self.request.user
        return initial

    def get_success_message(self, cleaned_data):
        item = self.object.item
        url = item.get_absolute_url()
        return f'Borrowed item <a href="{url}" class="alert-link">{item}</a>'

    def get_success_url(self):
        return self.request.path_info

    def form_valid(self, form):
        borrowed_by = form.cleaned_data['borrowed_by']
        item = form.cleaned_data['item']
        active_borrow = item.active_borrow
        if 'return' in self.request.POST:
            if active_borrow is None:
                messages.error(self.request, 'Can\'t return item that was not borrowed!')
                return redirect(self.request.path_info)
            elif active_borrow.borrowed_by != form.cleaned_data['borrowed_by']:
                messages.error(self.request, f'Item is currently borrowed by {form.cleaned_data["borrowed_by"]}, not by {self.object.borrowed_by}')
                return redirect(self.request.path_info)
            active_borrow.close(borrowed_by)
            url = item.get_absolute_url()
            messages.success(self.request, f'Successfully returned <a href="{url}" class="alert-link">{item}</a>')
            return redirect(self.request.path_info)
        if active_borrow is not None:
            url = item.get_absolute_url()
            messages.error(self.request, f'<a href="{url}" class="alert-link">{item}</a> is already borrowed by {active_borrow.borrowed_by}')
            return redirect(self.request.path_info)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = 'quick'
        return context


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
        context['item'] = get_object_or_404(models.Item, identifier=self.kwargs['identifier'])
        return context

    def get_success_message(self, cleaned_data):
        item = self.get_context_data()['item']
        url = item.get_absolute_url()
        return f'Borrowed item <a href="{url}" class="alert-link">{item}</a>'

    def get_success_url(self):
        return reverse_lazy('item-detail', kwargs={'identifier': self.object.item.identifier})

    def form_valid(self, form):
        item = self.get_context_data()['item']
        active_borrow = item.active_borrow
        if active_borrow is not None:
            url = item.get_absolute_url()
            messages.error(self.request, f'<a href="{url}" class="alert-link">{item}</a> is already borrowed by {active_borrow.borrowed_by}')
            return redirect(self.request.path_info)
        form.instance.item = item
        return super().form_valid(form)


class BorrowEditView(SuccessMessageMixin, UpdateView):
    model = models.Borrow
    form_class = forms.borrow.BorrowEditForm
    template_name_suffix = '_edit'
    success_message = 'Borrow successfully updated'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_closed:
            messages.error(request, 'Cannot edit Borrow as its already closed!')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('item-detail', kwargs={'identifier': self.object.item.identifier})


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
        if self.object.is_closed:
            messages.error(request, 'Borrow is already closed!')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.object.item
        return context

    def get_success_url(self):
        return reverse_lazy('item-detail', kwargs={'identifier': self.object.item.identifier})

    def form_valid(self, form):
        self.object.returned_at = now()
        self.object.save()
        item = self.object.item
        messages.success(self.request, f'You have returned {item}')
        return redirect(reverse_lazy('item-detail',
                                     kwargs={'identifier': self.get_context_data()['item'].identifier}))