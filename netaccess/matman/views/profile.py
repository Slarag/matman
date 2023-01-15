from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .. import models


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "matman/home.html"
    paginate_by = 5

    def get_user(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_user()
        context['user'] = user

        queries = {
            'my_materials': models.Material.objects.filter(owner=user),
            'borrowed': models.Material.objects.filter(borrows__borrowed_by=user,
                                                       borrows__returned_at__isnull=True),
            'lent': models.Material.objects.exclude(borrows=None).filter(owner=user,
                                                                         borrows__returned_at__isnull=True),
        }

        for name, query in queries.items():
            ordering = self.request.GET.get(f'{name}_orderby', 'identifier')
            query = query.order_by(ordering)
            paginator = Paginator(query, self.paginate_by)
            materials_page = self.request.GET.get(f'{name}_page')
            try:
                page_content = paginator.page(materials_page)
            except PageNotAnInteger:
                page_content = paginator.page(1)
            except EmptyPage:
                page_content = paginator.page(paginator.num_pages)
            context[name] = page_content
            context[f'{name}_total'] = len(query)

        return context


class ProfileView(HomeView):
    template_name = "matman/profile.html"

    def get_user(self):
        return User.objects.get(username=self.kwargs['user'])
