from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div, Button

from .. import models


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        # self.helper.add_input(Submit('cancel', 'Discard', css_class='btn btn-secondary', onclick=""))
        self.helper.add_input(Submit('submit', 'Post Comment', css_class='btn btn-primary'))
        self.helper.layout = Layout(Field('text', placeholder="Comment..."))

    class Meta:
        model = models.Comment
        fields = ['text']


class CommentEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = None
        self.helper.layout = Layout(Field('text', placeholder="Comment..."))

    class Meta:
        model = models.Comment
        fields = ['text']