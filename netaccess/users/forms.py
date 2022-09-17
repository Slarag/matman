from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit, Div

from . import models


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)
    department = forms.CharField(label='Department',
                                 widget=forms.TextInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(AuthenticationForm):
    next = forms.HiddenInput()
    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_action = reverse_lazy('login')
    # helper.form_class = 'container w-40'
    # helper.attrs = {'enctype': "multipart/form-data"}
    helper.form_tag = True
    helper.add_input(Submit('submit', 'Log-in', css_class='btn btn-primary'))
    helper.layout = Layout(
        Field('username'),#, css_class='d-flex'),
        Field('password'),#, css_class='d-flex'),
    )
