from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

from .. import models


class UserField(forms.CharField):
    def clean(self, value):
        try:
            return User.objects.get(username=value)
        except User.DoesNotExist:
            raise forms.ValidationError("Select a valid user")


class ItemField(forms.CharField):
    def clean(self, value):
        try:
            item = models.Material.objects.get(identifier=value)
        except models.Material.DoesNotExist:
            raise forms.ValidationError('Item does not exist')
        if not item.is_active:
            raise forms.ValidationError('Item was marked as not active')
        return item


class BorrowForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = models.Borrow
        fields = ['borrowed_by', 'usage_location', 'estimated_returndate', 'notes']
        widgets = {
            'estimated_returndate': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            # 'borrowed_by': forms.TextInput(),
        }


class QuickBorrowForm(forms.ModelForm):
    item = ItemField(widget=forms.TextInput(attrs={'autofocus': True}))
    borrowed_by = UserField(widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = models.Borrow
        fields = ['item', 'borrowed_by', 'usage_location', 'estimated_returndate']
        widgets = {
            'estimated_returndate': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


class BorrowEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    class Meta:
        model = models.Borrow
        fields = ['usage_location', 'estimated_returndate', 'notes']
        widgets = {
            'estimated_returndate': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
        }


class BorrowCloseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('returned_by'),
            Field('notes'),
        )

    class Meta:
        model = models.Borrow
        fields = ['returned_by', 'notes']
