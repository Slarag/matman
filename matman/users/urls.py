from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings

from . import views

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if getattr(settings, 'ALLOW_CHANGE_PASSWORD', False):
    urlpatterns += [
        path('password/change/', views.CustomPasswordChangeView.as_view(
            extra_context={'active': 'changepw'}
        ), name='password-change'),
        path('password/reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
        path('password/reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('password/reset/confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]

if getattr(settings, 'ALLOW_REGISTRATION', False):
    urlpatterns.append(path('register/', views.register, name='register'))
