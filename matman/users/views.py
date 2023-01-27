from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from . import forms


class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    success_message = 'Password updated successfully'
    success_url = '.'

def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})