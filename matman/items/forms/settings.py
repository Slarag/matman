from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

from .. import models


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['default_scheme'].queryset = models.Scheme.active
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('default_scheme'),
            Field('department'),
        )

    class Meta:
        model = models.UserProfile
        fields = ['default_scheme', 'department']