from django import forms
from django.db.models import TextChoices
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div

from .. import models


class ItemCreateForm(forms.ModelForm):
    reference = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheme'].queryset = models.Scheme.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('reference'),
            Div(
                Div(Field('serial_number', placeholder="Serial Number", autofocus=True), css_class='col'),
                Div(Field('part_number', placeholder='Item Number'), css_class='col'),
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
                Field('description', placeholder='Enter item description here (supports markdown syntax)...'),
            ),
        )

    class Meta:
        model = models.Item
        fields = ['serial_number', 'part_number', 'revision', 'manufacturer', 'description', 'scheme', 'owner',
                  'short_text', 'tags', 'is_active', 'location']


class ItemEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Div(
                Div(Field('serial_number', placeholder="Serial Number", autofocus=True), css_class='col'),
                Div(Field('part_number', placeholder='Item Number'), css_class='col'),
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
                Field('description', placeholder='Enter item description here (supports markdown syntax)...'),
            ),
        )

    class Meta:
        model = models.Item
        fields = ['serial_number', 'part_number', 'revision', 'manufacturer', 'description', 'owner',
                  'short_text', 'tags', 'is_active', 'location']


class SearchForm(forms.Form):
    search = forms.CharField(max_length=200, required=False)
    active_only = forms.BooleanField(initial=True, label='Show active items only', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True


class ItemCsvImportForm(forms.Form):
    class Delimiter(TextChoices):
        TAB = '\t', 'Tab'
        SEMICOLON = ';', 'Semicolon'
        COMMA = ',', 'Comma'
        SPACE = ' ', 'Space'

    scheme = forms.ModelChoiceField(required=True, queryset=models.Scheme.active)
    file = forms.FileField()
    delimiter = forms.ChoiceField(choices=Delimiter.choices, required=True, initial=Delimiter.SEMICOLON)
    tag_delimiter = forms.ChoiceField(choices=Delimiter.choices, required=True, initial=Delimiter.COMMA)
    set_owner = forms.BooleanField(label='Make me the owner of all newly created items if no owner was specified',
                                   required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def clean_tag_delimiter(self):
        tag_delimiter = self.cleaned_data['tag_delimiter']
        delimiter = self.cleaned_data['delimiter']
        if tag_delimiter == delimiter:
            self.add_error('tag_delimiter', 'tag delimiter must be different to standard delimiter')

        return tag_delimiter
