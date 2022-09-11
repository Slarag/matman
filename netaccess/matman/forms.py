from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div

from . import models


class BorrowForm(forms.ModelForm):
    class Meta:
        model = models.Borrow
        fields = ['usage_location', 'notes']


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheme'].queryset = models.Scheme.objects.filter(is_active=True)

    helper = FormHelper()
    # helper.form_method = 'post'
    # helper.attrs = {'enctype': "multipart/form-data"}
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div(Field('serial_number', placeholder="Serial Number"), css_class='col'),
            Div(Field('material_number', placeholder='Material Number'), css_class='col'),
            Div(Field('manufacturer', placeholder='Manufacturer'), css_class='col'),
            css_class='row'),
        Div(
            Div(Field('scheme'), css_class='col'),
            Div(Field('owner'), css_class='col'),
            css_class='row g-3'),
        Div(
            Field('tags', placeholder='tag1,tag2,tag3,...'),
            Field('description', placeholder='Enter material description here (supports markdown syntax)...'),
            'is_active'),
    )

    class Meta:
        model = models.Material
        fields = ['serial_number', 'material_number', 'manufacturer', 'description', 'scheme', 'owner', 'tags',
                  'is_active']


PictureFormset = forms.inlineformset_factory(models.Material, models.MaterialPicture,
                                             fields=['file', 'description'], extra=5, max_num=5, can_order=True)
PictureFormset.helper = FormHelper()
PictureFormset.helper.form_tag = False


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['default_scheme'].queryset = models.Scheme.objects.filter(is_active=True)

    class Meta:
        model = models.UserProfile
        fields = ['default_scheme']


class SchemeCreateForm(forms.ModelForm):
    helper = FormHelper()
    # helper.form_method = 'post'
    # helper.attrs = {'enctype': "multipart/form-data"}
    helper.form_tag = False
    helper.layout = Layout(
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
    helper = FormHelper()
    # helper.form_method = 'post'
    # helper.attrs = {'enctype': "multipart/form-data"}
    helper.form_tag = False
    helper.layout = Layout(
        Field('name', placeholder='Name'),
        Field('description', placeholder='Description'),
        Field('is_active'),
    )

    class Meta:
        model = models.Scheme
        fields = ['name', 'description', 'is_active']