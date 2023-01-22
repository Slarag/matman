from django.urls import path, include
# from django.views.generic import RedirectView
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    path('', views.borrow.QuickBorrowView.as_view(), name='quick-borrow'),

    path('comment/<int:pk>/edit', views.comment.CommentEditView.as_view(), name='comment-edit'),

    path('material', views.material.MaterialListView.as_view(), name='list-material'),
    path('material/add', views.material.MaterialCreateView.as_view(), name='add-material'),
    path('material/<slug:identifier>/detail', views.material.MaterialDetailView.as_view(), name='material-detail'),
    path('material/<slug:identifier>/edit', views.material.MaterialEditView.as_view(), name='material-edit'),
    path('material/<slug:identifier>/borrow', views.borrow.BorrowCreateView.as_view(), name='borrow'),
    path('material/search', views.material.search, name='search'),

    path('borrow/<int:pk>/edit', views.borrow.BorrowEditView.as_view(), name='borrow-edit'),
    path('borrow/<int:pk>/close', views.borrow.BorrowCloseView.as_view(), name='return'),

    path('home', views.profile.HomeView.as_view(), name='home'),
    path('profile/<slug:user>', views.profile.ProfileView.as_view(), name='profile'),

    path('utils/tags/', views.ajax.tag_suggestions, name='tag-suggestions'),

    path('schemes/list', views.scheme.SchemeListView.as_view(), name='list-schemes'),
    path('schemes/add', views.scheme.SchemeCreateView.as_view(), name='add-scheme'),
    path('schemes/<int:pk>/edit', views.scheme.SchemeEditView.as_view(), name='edit-scheme'),

    path('settings', views.settings.SettingsView.as_view(), name='profile-settings'),
    ]
