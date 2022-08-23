from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchQuery

from .models import Material, Borrow, Scheme, UserProfile
from .forms import BorrowForm, SearchForm


class MaterialAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Material
    template_name_suffix = '_create'
    fields = ['serial_number', 'material_number', 'manufacturer', 'description', 'scheme', 'owner', 'tags',
              'is_active']

    def get_initial(self):
        initial = super().get_initial().copy()
        initial['owner'] = self.request.user
        initial['scheme'] = self.request.user.profile.default_scheme
        return initial

    def get_success_message(self, cleaned_data):
        return f'Successfully created material "{self.object}"'

    def get_success_url(self):
        if 'add_other' in self.request.POST:
            return reverse_lazy('add-material')
        return super().get_success_url()

    def form_valid(self, form):
        scheme = form.instance.scheme
        form.instance.identifier = scheme.get_next_id()
        return super().form_valid(form)


# Important: No login required for details
class MaterialDetailView(DetailView):
    model = Material
    template_name_suffix = '_detail'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'


class MaterialEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Material
    template_name_suffix = '_edit'
    fields = ['serial_number', 'material_number', 'manufacturer', 'description', 'scheme', 'location', 'owner',
              'tags', 'is_active']
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'

    def get_success_message(self, cleaned_data):
        return f'Successfully updated material "{self.object}"'


@login_required
def borrow(request, identifier):
    material = get_object_or_404(Material, identifier=identifier)
    active_borrow = material.get_active_borrow()
    if active_borrow:
        messages.error(request, f'{material} is already borrowed by {active_borrow.borrowed_by}')
        return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
    if request.method == 'POST':
        if 'yes' in request.POST:
            form = BorrowForm(request.POST)
            if form.is_valid():
                b = Borrow(item=material, borrowed_by=request.user)
                b.save()
                messages.success(request, f'{material} successfully borrowed')
                return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
        else:
            return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
    else:
        form = BorrowForm(initial={'object': material})
    return render(request, 'matman/borrow.html', {'material': material})


@login_required
def end_borrow(request, identifier):
    material = get_object_or_404(Material, identifier=identifier)
    active_borrow = material.get_active_borrow()
    if not active_borrow:
        messages.error(request, f'You have currently not borrowed { material }!')
        return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if 'yes' in request.POST:
            if form.is_valid():
                active_borrow.returned_at = now()
                active_borrow.save()
                messages.success(request, f'You have returned {material} to {material.owner}')
                return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
        else:
            return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
    else:
        form = BorrowForm(active_borrow)
    return render(request, 'matman/borrow_done.html', {'material': material})


class MaterialListView(ListView):
    model = Material
    template_name_suffix = '_list'
    fields = ['serial_number', 'material_number', 'manufacturer', 'scheme', 'owner', 'tags', 'is_active']
    paginate_by = 50


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "matman/home.html"


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "matman/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = User.objects.get(username=self.kwargs['user'])
        return context


def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                material = Material.objects.get(identifier=query)
                return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
            except ObjectDoesNotExist:
                pass
            results = Material.objects.annotate(
                search=SearchVector('identifier', 'serial_number', 'material_number', 'manufacturer', 'description',
                                    'location', 'tags__name'),
                query=SearchQuery(query, search_type='websearch')
            )
            # search_vector = SearchVector('identifier', 'serial_number', 'material_number', 'manufacturer',
            #                              'description', 'location', 'tags__name')
            # search_query = SearchQuery(query)
            # results = Material.objects.annotate(
            #     similarity=TrigramSimilarity('tags__name', query) + TrigramSimilarity('description', query),
            #     # search_vector=search_vector, #search_query=query
            # ).filter(similarity__gt=0.1).order_by('-similarity')
    return render(request,
                  'matman/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


class SchemeListView(ListView):
    model = Scheme
    template_name_suffix = '_list'
    fields = ['name', 'prefix', 'numlen', 'postfix', 'is_active']
    paginate_by = 50


class SchemeAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Scheme
    template_name_suffix = '_create'
    fields = ['name', 'prefix', 'numlen', 'postfix', 'is_active']

    def get_success_message(self, cleaned_data):
        return f'Successfully created scheme "{self.object}"'

    def get_success_url(self):
        if 'add_other' in self.request.POST:
            return reverse_lazy('add-scheme')
        return super().get_success_url()


class SchemeEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Scheme
    template_name_suffix = '_edit'
    fields = ['name', 'prefix', 'numlen', 'postfix', 'is_active']
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'

    def get_success_message(self, cleaned_data):
        return f'Successfully updated scheme "{self.object}"'


class SettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name_suffix = '_edit'
    fields = ['default_scheme']
    success_message = 'Profile settings updated successfully'

    def get_success_url(self):
        return reverse_lazy('profile-settings')

    def get_object(self, queryset=None):
        return self.request.user.profile
