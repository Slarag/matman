from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .. import models


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "items/profile.html"
    is_home = True

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user()

        context['bookmarked'] = []
        if self.request.user.is_authenticated:
            context['bookmarked'] = self.request.user.profile.bookmarks.all()

        context['user'] = user
        context['active'] = 'home' if self.is_home else ''
        context['rubrics'] = {
            'borrowed': {
                'query': models.Material.objects.filter(borrows__borrowed_by=user,
                                                        borrows__returned_at__isnull=True),
                'title': 'Borrowed Items',
            },
            'lent': {
                'query': models.Material.objects.exclude(borrows=None).filter(owner=user,
                                                                              borrows__returned_at__isnull=True),
                'title': 'Items borrowed to/by others',
            },
            'bookmarked': {
                'query': user.profile.bookmarks.all(),
                'title': 'Bookmarked Items',
            },
            'owned': {
                'query': models.Material.objects.filter(owner=user),
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
            try:
                page = paginator.page(self.request.GET.get(f'{name}_page', 1))
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            data['object_list'] = page

        context['is_home'] = self.is_home

        return context


class ProfileView(HomeView):
    is_home = False

    def get_user(self):
        return User.objects.get(username=self.kwargs['user'])
