

class ActiveMixin:
    active_context: str = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = self.active_context
        return context


class ViewFormsetHelperMixin:
    formset_helper = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.formset_helper is not None:
            context['formset_helper'] = self.formset_helper()
        return context
