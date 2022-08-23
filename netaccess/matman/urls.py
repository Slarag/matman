from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('material', views.MaterialListView.as_view(), name='list-material'),
    path('material/add', views.MaterialAddView.as_view(), name='add-material'),
    path('material/<slug:identifier>/detail', views.MaterialDetailView.as_view(), name='material-detail'),
    path('material/<slug:identifier>/edit', views.MaterialEditView.as_view(), name='material-edit'),
    path('material/<slug:identifier>/borrow', views.borrow, name='borrow'),
    path('material/<slug:identifier>/return', views.end_borrow, name='return'),
    path('material/search', views.search, name='search'),
    path('home', views.HomeView.as_view(), name='home'),
    path('profile/<slug:user>', views.ProfileView.as_view(), name='profile'),

    path('schemes/list', views.SchemeListView.as_view(), name='list-schemes'),
    path('schemes/add', views.SchemeAddView.as_view(), name='add-scheme'),
    path('schemes/<int:pk>/edit', views.SchemeEditView.as_view(), name='edit-scheme'),

    path('settings', views.SettingsView.as_view(), name='profile-settings'),
    ]