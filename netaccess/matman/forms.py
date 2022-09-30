import datetime

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div, Button

from . import models


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
                Field('tags', placeholder='tag1,tag2,tag3,...'),
                Field('description', placeholder='Enter material description here (supports markdown syntax)...'),
                'is_active'),
        )

    class Meta:
        model = models.Material
        fields = ['serial_number', 'material_number', 'revision', 'manufacturer', 'description', 'scheme', 'owner',
                  'short_text', 'tags', 'is_active', 'location']


PictureFormset = forms.inlineformset_factory(models.Material, models.MaterialPicture,
                                             fields=['file', 'title', 'description'],
                                             extra=1, can_order=True)
PictureFormset.ordering_widget = forms.HiddenInput()


class PictureFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.form_class = 'formset-container'
        self.layout = Layout(
            Div(
                Field('ORDER'),
                Field('title', placeholder='Title'),
                Field('description'),
                Field('file'),
                Field('DELETE'),
                # id and material are automatically added when form is initialized with instance keyword
                Field('id'),
                Field('material'),
                css_class='card p-2 m-1 draggable formset-form',
                draggable="true",
            ),
        )
        self.render_required_fields = True


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['default_scheme'].queryset = models.Scheme.objects.filter(is_active=True)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Field('default_scheme'),
            Field('location', placeholder='Describe where people usually can find you...'),
            Field('initials', placeholder='Your Initials')
        )

    class Meta:
        model = models.UserProfile
        fields = ['default_scheme', 'location', 'initials']


class SchemeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create', css_class='btn btn-primary'))
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
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary'))
        self.helper.layout = Layout(
            Field('name', placeholder='Name'),
            Field('description', placeholder='Description'),
            Field('is_active'),
        )

    class Meta:
        model = models.Scheme
        fields = ['name', 'description', 'is_active']