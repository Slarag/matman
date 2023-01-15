from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div, Button

from .. import models


class BorrowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button('cancel', 'No, go back', css_class='btn btn-secondary', onclick="history.back()"))
        self.helper.add_input(Submit('submit', 'Yes, borrow', css_class='btn btn-primary'))

    class Meta:
        model = models.Borrow
        fields = ['borrowed_by', 'usage_location', 'estimated_returndate', 'notes']


class BorrowEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="history.back()"))
        self.helper.add_input(Submit('submit', 'Update', css_class='btn btn-primary'))

    class Meta:
        model = models.Borrow
        fields = ['usage_location', 'estimated_returndate', 'notes']


class BorrowCloseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('returned_by'),
            Field('notes'),
        )
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="history.back()"))
        self.helper.add_input(Submit('close', 'Return & Close', css_class='btn btn-primary'))

    class Meta:
        model = models.Borrow
        fields = ['returned_by', 'notes']