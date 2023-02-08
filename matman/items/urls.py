from django.urls import path, include
# from django.views.generic import RedirectView
# from django.views.defaults import page_not_found

from . import views

urlpatterns = [
    path('', views.borrow.QuickBorrowView.as_view(), name='quick-borrow'),

    path('comment/<int:pk>/edit', views.comment.CommentEditView.as_view(), name='comment-edit'),

    path('item', views.item.ItemListView.as_view(), name='list-item'),
    path('item/add', views.item.ItemCreateView.as_view(), name='add-item'),
    path('item/<slug:identifier>/detail', views.item.ItemDetailView.as_view(), name='item-detail'),
    path('item/<slug:identifier>/edit', views.item.ItemEditView.as_view(), name='item-edit'),
    path('item/<slug:identifier>/borrow', views.borrow.BorrowCreateView.as_view(), name='borrow'),

    path('borrow/<int:pk>/edit', views.borrow.BorrowEditView.as_view(), name='borrow-edit'),
    path('borrow/<int:pk>/close', views.borrow.BorrowCloseView.as_view(), name='return'),

    path('home', views.profile.HomeView.as_view(), name='home'),
    path('profile/<slug:user>', views.profile.ProfileView.as_view(), name='profile'),

    path('utils/tags/', views.ajax.tag_suggestions, name='tag-suggestions'),
    path('utils/users/', views.ajax.user_suggestions, name='user-suggestions'),
    path('utils/bookmark/', views.ajax.toggle_bookmark, name='toggle-bookmark'),

    path('schemes/list', views.scheme.SchemeListView.as_view(), name='list-schemes'),
    path('schemes/add', views.scheme.SchemeCreateView.as_view(), name='add-scheme'),
    path('schemes/<int:pk>/edit', views.scheme.SchemeEditView.as_view(), name='edit-scheme'),

    path('settings', views.settings.SettingsView.as_view(), name='profile-settings'),
    path('about', views.settings.AboutView.as_view(), name='about'),
    ]
