import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


@login_required
def dashboard(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard',
                   'ssh_keys_total': request.user.pubkeys.all().count(),
                   'ssh_keys_active': request.user.pubkeys.filter(expiration_date__lte=datetime.datetime.now().date()).count(),
                   })


@login_required
def keys_view(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'keys'})


@login_required
def edit_view(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard'})


@login_required
def dhcp_overview(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard'})


@login_required
def dhcp_overview(request):
    return render(request,
                  'users/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objet.create(user=new_user, department=user_form.cleaned_data['department'])
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'registration/edit.html', {'user_form': user_form, 'profile_form': profile_form})
