from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    # path('material'),
    path('material/add', views.MaterialAddView.as_view(), name='add-material'),
    path('material/<slug:identifier>/detail', views.MaterialDetailView.as_view(), name='material-detail'),
    path('material/<slug:identifier>/edit', views.MaterialEditView.as_view(), name='material-edit'),
    #
    # path('locations'),
    # path('locations/add'),
    # path('locations/<slug:identifier>/detail'),
    # path('locations/<slug:identifier>/edit'),
    # path('locations/<slug:identifier>/delete'),
    #
    # path('departments'),
    # path('departments/add'),
    # path('departments/<slug:identifier>/detail'),
    # path('departments/<slug:identifier>/edit'),
    # path('departments/<slug:identifier>/delete'),
    #
    # path('borrow'),
    # path('borrow/add'),
    # path('borrow/<slug:identifier>/detail'),
    # path('borrow/<slug:identifier>/edit'),
    # # path('borrow/<slug:identifier>/delete'),
    # path('borrow/<slug:identifier>/return'),
    ]