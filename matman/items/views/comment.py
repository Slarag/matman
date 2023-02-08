from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .. import models
from .. import forms


class CommentEditView(SuccessMessageMixin, DeletionMixin, UpdateView):
    model = models.Comment
    template_name_suffix = '_edit'
    form_class = forms.comment.CommentEditForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        print(self.request.POST)

        if self.request.POST.get('action') == 'delete':
            return self.delete(request, *args, **kwargs)

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.warning(request, 'Comment deleted')
        return result

    def get_success_url(self):
        return reverse_lazy('item-detail', kwargs={'identifier': self.object.item.identifier})

    def get_success_message(self, cleaned_data):
            return 'Comment successfully updated'
