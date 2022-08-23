from django import forms
from django.contrib.auth.models import User

from . import models


class BorrowForm(forms.ModelForm):
    class Meta:
        model = models.Borrow
        fields = []


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True})
    )
