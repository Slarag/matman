from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

from .. import models


class SchemeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.add_input(Submit('submit', 'Create', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Field('name', placeholder='Name'),
            Field('description', placeholder='Description'),
            Div(
                Div(Field('prefix', placeholder="Prefix"), css_class='col'),
                Div(Field('numlen', placeholder='Numlen'), css_class='col'),
                Div(Field('postfix', placeholder='postfix'), css_class='col'),
                css_class='row'),
            Field('is_active'),
        )

    class Meta:
        model = models.Scheme
        fields = ['name', 'description', 'prefix', 'numlen', 'postfix', 'is_active']


class SchemeEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Field('name', placeholder='Name'),
            Field('description', placeholder='Description'),
            Field('is_active'),
        )

    class Meta:
        model = models.Scheme
        fields = ['name', 'description', 'is_active']