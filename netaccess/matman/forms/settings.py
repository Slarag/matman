from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div, Button

from .. import models


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