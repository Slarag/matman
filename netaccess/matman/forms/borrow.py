from django import forms
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div, Button

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
        self.helper.add_input(Button('cancel', 'No, go back', css_class='btn btn-secondary', onclick="history.back()"))
        self.helper.add_input(Submit('submit', 'Yes, borrow', css_class='btn btn-primary'))

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
        # self.helper.add_input(Submit('borrow', 'Borrow', css_class='btn btn-primary'))
        # self.helper.add_input(Submit('return', 'Return', css_class='btn btn-secondary'))

    class Meta:
        model = models.Borrow
        fields = ['item', 'borrowed_by', 'usage_location', 'estimated_returndate']
        # field_classes = {
        #     'item': forms.CharField,
        #     'borrowed_by': forms.CharField,
        # }
        widgets = {
            'estimated_returndate': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'
                       }),
            # 'item': forms.TextInput(),
            # 'borrowed_by': forms.TextInput(),
        }


class BorrowEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="history.back()"))
        self.helper.add_input(Submit('submit', 'Update', css_class='btn btn-primary'))

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
        self.helper.layout = Layout(
            Field('returned_by'),
            Field('notes'),
        )
        self.helper.add_input(Button('cancel', 'Cancel', css_class='btn btn-secondary', onclick="history.back()"))
        self.helper.add_input(Submit('close', 'Return & Close', css_class='btn btn-primary'))

    class Meta:
        model = models.Borrow
        fields = ['returned_by', 'notes']
