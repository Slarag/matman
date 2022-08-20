from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=True)),

    path('keys/', views.SshPubKeyListView.as_view(), name='key-list'),
    path('keys/<int:pk>/detail/', views.KeyDetailView.as_view(), name='key-detail'),
    path('keys/<int:pk>/update/', views.KeyEditView.as_view(), name='key-update'),
    path('keys/<int:pk>/delete/', views.KeyDeleteView.as_view(), name='key-delete'),
    path('keys/create/', views.KeyCreateView.as_view(), name='key-create'),
]
