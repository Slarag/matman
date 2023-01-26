from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

# from .views import LoginView
# from django.views.generic import RedirectView
# from django.contrib.auth import views as auth_views
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(
        extra_context={
            'registration_allowed': getattr(settings, 'ALLOW_REGISTRATION', False),
            'reset_allowed': getattr(settings, 'ALLOW_CHANGE_PASSWORD', False),
        }
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if getattr(settings, 'ALLOW_CHANGE_PASSWORD', False):
    urlpatterns += [
        path('password/change/', views.CustomPasswordChangeView.as_view(), name='password-change'),
        path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
        path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('password/reset/confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]

if getattr(settings, 'ALLOW_REGISTRATION', False):
    urlpatterns.append(path('register/', views.register, name='register'))
