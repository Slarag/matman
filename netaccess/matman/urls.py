from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    path('material', views.MaterialListView.as_view(), name='list-material'),
    path('material/add', views.MaterialAddView.as_view(), name='add-material'),
    path('material/<slug:identifier>/detail', views.MaterialDetailView.as_view(), name='material-detail'),
    path('material/<slug:identifier>/edit', views.MaterialEditView.as_view(), name='material-edit'),
    path('material/<slug:identifier>/borrow', views.borrow, name='borrow'),
    path('material/<slug:identifier>/return', views.end_borrow, name='return'),
    path('material/search', views.search, name='search'),
    path('home', views.HomeView.as_view(), name='home'),
    path('profile/<slug:user>', views.ProfileView.as_view(), name='profile'),
    #
    # path('departments'),
    # path('departments/add'),
    # path('departments/<slug:identifier>/detail'),
    # path('departments/<slug:identifier>/edit'),
    # path('departments/<slug:identifier>/delete'),
    #
    ]