from django import forms
from django.contrib.auth.models import User

from . import models


class BorrowForm(forms.ModelForm):
    class Meta:
        model = models.Borrow
        fields = ['usage_location']


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class MaterialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheme'].queryset = models.Scheme.objects.filter(is_active=True)

    class Meta:
        model = models.Material
        fields = ['serial_number', 'material_number', 'manufacturer', 'description', 'scheme', 'owner', 'tags',
                  'is_active']


PictureFormset = forms.inlineformset_factory(models.Material, models.MaterialPicture,
                                             fields=['file', 'description'], extra=5, max_num=5, can_order=True)


class SettingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['default_scheme'].queryset = models.Scheme.objects.filter(is_active=True)

    class Meta:
        model = models.UserProfile
        fields = ['default_scheme']