from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .. import models


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "matman/home.html"

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user()
        context['user'] = user
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
            data['page_items'] = int(self.request.GET.get(f'{name}_items', '10'))
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
            paginator = Paginator(data['query'], data['page_items'])
            try:
                data['page'] = paginator.page(self.request.GET.get(f'{name}_page', 1))
            except PageNotAnInteger:
                data['page'] = paginator.page(1)
            except EmptyPage:
                data['page'] = paginator.page(paginator.num_pages)

        return context


class ProfileView(HomeView):
    template_name = "matman/profile.html"

    def get_user(self):
        return User.objects.get(username=self.kwargs['user'])
