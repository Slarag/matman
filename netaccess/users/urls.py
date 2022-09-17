from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.views.generic import RedirectView
# from django.contrib.auth import views as auth_views
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=LoginForm),
         name='login'
         ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(
        extra_context={'sidebar_sel': 'password'}),
         name='password-change'),
    # path('password_change/', RedirectView.as_view(pattern_name='password-change-new', permanent=True)),


    # path('register/', views.register, name='register'),
    # path('profile/edit', views.edit_profile, name='profile-edit'),
]
