from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div, Button

from .. import models


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_tag = True
        self.helper.disable_csrf = True
        self.helper.add_input(Submit('submit', 'Search', css_class='btn btn-primary'))


class MaterialForm(forms.ModelForm):
    reference = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheme'].queryset = models.Scheme.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('reference'),
            Div(
                Div(Field('serial_number', placeholder="Serial Number"), css_class='col'),
                Div(Field('material_number', placeholder='Material Number'), css_class='col'),
                Div(Field('revision', placeholder='Revision'), css_class='col'),
                Div(Field('manufacturer', placeholder='Manufacturer'), css_class='col'),
                css_class='row'),
            Div(
                Div(Field('location', placeholder='Location'), css_class='col'),
                Div(Field('scheme'), css_class='col'),
                Div(Field('owner'), css_class='col'),
                css_class='row g-3'),
            Div(
                Field('short_text', placeholder='Short description'),
                Field('tags', placeholder='tag1,tag2,tag3,...', autocomplete='off'),
                Field('is_active'),
                Field('description', placeholder='Enter material description here (supports markdown syntax)...'),
            ),
        )

    class Meta:
        model = models.Material
        fields = ['serial_number', 'material_number', 'revision', 'manufacturer', 'description', 'scheme', 'owner',
                  'short_text', 'tags', 'is_active', 'location']


class MaterialEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('reference'),
            Div(
                Div(Field('serial_number', placeholder="Serial Number"), css_class='col'),
                Div(Field('material_number', placeholder='Material Number'), css_class='col'),
                Div(Field('revision', placeholder='Revision'), css_class='col'),
                Div(Field('manufacturer', placeholder='Manufacturer'), css_class='col'),
                css_class='row'),
            Div(
                Div(Field('location', placeholder='Location'), css_class='col'),
                Div(Field('owner'), css_class='col'),
                css_class='row g-3'),
            Div(
                Field('short_text', placeholder='Short description'),
                Field('tags', placeholder='tag1,tag2,tag3,...', autocomplete='off'),
                Field('is_active'),
                Field('description', placeholder='Enter material description here (supports markdown syntax)...'),
            ),
        )

    class Meta:
        model = models.Material
        fields = ['serial_number', 'material_number', 'revision', 'manufacturer', 'description', 'owner',
                  'short_text', 'tags', 'is_active', 'location']

