from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q

from .. import models
from .mixins import ActiveMixin


class HomeView(ActiveMixin, LoginRequiredMixin, TemplateView):
    template_name = "items/profile.html"
    is_home = True
    active_context = 'home'

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user()

        context['bookmarked'] = []
        if self.request.user.is_authenticated:
            context['bookmarked'] = self.request.user.profile.bookmarks.all()

        context['user'] = user
        context['rubrics'] = {
            'borrowed': {
                'query': (
                    models.Item.objects
                    .filter(borrows__borrowed_by=user,borrows__returned_at__isnull=True)
                    .annotate(bookmarked=Q(bookmarked_by__in=[user.profile]))
                ),
                'title': 'Borrowed Items',
            },
            'lent': {
                'query': (
                    models.Item.objects
                    .exclude(borrows=None)
                    .filter(owner=user, borrows__returned_at__isnull=True)
                    .annotate(bookmarked=Q(bookmarked_by__in=[user.profile]))
                ),
                'title': 'Items borrowed to/by others',
            },
            'bookmarked': {
                'query': (
                    user.profile.bookmarks.all()
                    .annotate(bookmarked=Q(bookmarked_by__in=[user.profile]))
                ),
                'title': 'Bookmarked Items',
            },
            'owned': {
                'query': (
                    models.Item.objects
                    .filter(owner=user)
                    .annotate(bookmarked=Q(bookmarked_by__in=[user.profile]))
                ),
                'title': 'Owned Items',
            },
        }

        for name, data in context['rubrics'].items():
            data['items'] = self.request.GET.get(f'{name}_items', '10')
            data['is_open'] = True if self.request.GET.get(f'{name}_open', 'false') == 'true' else False
            orderby = self.request.GET.get(f'{name}_orderby', 'identifier')
            data['orderby'] = orderby
            direction = self.request.GET.get(f'{name}_direction', 'asc')
            if direction not in ['asc', 'desc']:
                direction = 'asc'
            if direction == 'desc':
                orderby = f'-{orderby}'
            data['direction'] = direction
            data['query'] = data['query'].order_by(orderby)
            data['total'] = data['query'].count()
            paginator = Paginator(data['query'], data['items'])
            page_number = self.request.GET.get(f'{name}_page', 1)
            try:
                page = paginator.page(page_number)
                page_obj = paginator.get_page(page_number)
            except PageNotAnInteger:
                page = paginator.page(1)
                page_obj = paginator.get_page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
                page_obj = paginator.get_page(paginator.num_pages)
            data['page_obj'] = page_obj
            data['object_list'] = page

        context['is_home'] = self.is_home

        return context


class ProfileView(HomeView):
    is_home = False
    active_context = ''

    def get_user(self):
        return User.objects.get(username=self.kwargs['user'])
