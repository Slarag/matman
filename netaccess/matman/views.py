from collections import namedtuple
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.postgres.search import SearchVector, TrigramSimilarity, SearchQuery, SearchRank

from . import models
from . import forms


CronObject = namedtuple('CronObject', ['timestamp', 'type', 'object'])


class MaterialAddView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Material
    template_name_suffix = '_create'
    form_class = forms.MaterialForm
    formset_class = forms.PictureFormset
    formset_helper = forms.PictureFormSetHelper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset_helper'] = self.formset_helper()
        return context

    def get_initial(self):
        initial = super().get_initial().copy()
        initial['owner'] = self.request.user
        initial['scheme'] = self.request.user.profile.default_scheme
        return initial

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully created material <a href="{url}" class="alert-link">{self.object}</a>'

    def get_success_url(self):
        if 'add_other' in self.request.POST:
            return reverse_lazy('add-material')
        return super().get_success_url()

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(instance=form.instance)

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(self.request.POST, self.request.FILES)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)

        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance=form.instance
        formset.save()

        return super().form_valid(form)

    def form_invalid(self, form, formset):
        messages.error(self.request, 'An error occurred while updating the material')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


# Important: No login required for details
class MaterialDetailView(DetailView):
    model = models.Material
    template_name_suffix = '_detail'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'
    form_class = forms.CommentForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        cb = [CronObject(x.creation_date, 'comment', x) for x in self.object.comments.all().order_by('-creation_date')]
        cb += [CronObject(x.borrowed_at, 'borrow', x) for x in self.object.borrows.all().order_by('-borrowed_at')]
        cb.sort(key=lambda x: x.timestamp)
        context['comments_borrows'] = cb
        context['comment_form'] = self.kwargs.get('comment_form', forms.CommentForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form = self.form_class(self.request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.material = self.object
            comment.author = request.user
            comment.save()
            url = self.object.get_absolute_url()
            messages.success(
                self.request,
                f'Successfully created commend on material <a href="{url}" class="alert-link">{self.object}</a>'
            )
            return self.render_to_response(self.get_context_data())

        messages.error(self.request, 'Error while creating comment')
        return self.render_to_response(
            self.get_context_data(comment_form=form)
        )


class MaterialEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Material
    template_name_suffix = '_edit'
    form_class = forms.MaterialForm
    formset_class = forms.PictureFormset
    formset_helper = forms.PictureFormSetHelper
    related_name = 'pictures'
    slug_field = 'identifier'
    slug_url_kwarg = 'identifier'

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully updated material <a href="{url}" class="alert-link">{self.object}</a>'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset_helper'] = self.formset_helper()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(instance=form.instance)

        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(self.request.POST, self.request.FILES, instance=form.instance)

        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)

        return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.save()

        return super().form_valid(form)

    def form_invalid(self, form, formset):
        messages.error(self.request, 'An error occurred while updating the material')
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )


class BorrowCreateView(SuccessMessageMixin, CreateView):
    model = models.Borrow
    form_class = forms.BorrowForm
    template_name_suffix = '_create'

    def get_initial(self):
        initial = super().get_initial().copy()
        initial['estimated_returndate'] = (now() + datetime.timedelta(days=7)).date()
        if self.request.user.is_authenticated:
            initial['borrowed_by'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['material'] = get_object_or_404(models.Material, identifier=self.kwargs['identifier'])
        return context

    def get_success_message(self, cleaned_data):
        material = self.get_context_data()['material']
        url = material.get_absolute_url()
        return f'Borrowed material <a href="{url}" class="alert-link">{material}</a>'

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.item.identifier})

    def form_valid(self, form):
        form.instance.item = self.get_context_data()['material']
        return super().form_valid(form)


class BorrowEditView(SuccessMessageMixin, UpdateView):
    model = models.Borrow
    form_class = forms.BorrowEditForm
    template_name_suffix = '_edit'
    success_message = 'Borrow successfully updated'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.returned_at is not None:
            messages.error(request, 'Cannot edit Borrow as its already closed!')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.item.identifier})


class BorrowCloseView(SuccessMessageMixin, UpdateView):
    model = models.Borrow
    form_class = forms.BorrowCloseForm
    template_name_suffix = '_close'
    success_message = 'Borrow successfully closed'

    def get_initial(self):
        initial = super().get_initial().copy()
        if self.request.user.is_authenticated:
            initial['returned_by'] = self.request.user
        return initial

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.returned_at is not None:
            messages.error(request, 'Borrow is already closed!')
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material'] = self.object.item
        return context

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.item.identifier})

    def form_valid(self, form):
        if 'close' in self.request.POST:
            self.object.returned_at = now()
            self.object.save()
            material = self.object.item
            messages.success(self.request, f'You have returned {material}')
        return redirect(reverse_lazy('material-detail',
                                     kwargs={'identifier': self.get_context_data()['material'].identifier}))


class MaterialListView(ListView):
    model = models.Material
    template_name_suffix = '_list'
    fields = ['serial_number', 'material_number', 'manufacturer', 'scheme', 'owner', 'tags', 'is_active']
    paginate_by = 20

    def get_ordering(self):
        ordering = self.request.GET.get('orderby', '-identifier')
        return ordering


class CommentEditView(SuccessMessageMixin, DeletionMixin, UpdateView):
    model = models.Comment
    template_name_suffix = '_edit'
    form_class = forms.CommentEditForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(self.queryset)
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        print(self.request.POST)

        if self.request.POST.get('action') == 'delete':
            return self.delete(request, *args, **kwargs)

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.warning(request, 'Comment deleted')
        return result

    def get_success_url(self):
        return reverse_lazy('material-detail', kwargs={'identifier': self.object.material.identifier})

    def get_success_message(self, cleaned_data):
            return 'Comment successfully updated'


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

        return context


class ProfileView(HomeView):
    template_name = "matman/profile.html"

    def get_user(self):
        return User.objects.get(username=self.kwargs['user'])



def search(request):
    form = forms.SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = forms.SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            try:
                material = models.Material.objects.get(identifier=query)
                return redirect(reverse_lazy('material-detail', kwargs={'identifier': material.identifier}))
            except ObjectDoesNotExist:
                pass
            search_vector = SearchVector('identifier', 'short_text', 'serial_number', 'material_number',
                                         'manufacturer', 'description', 'location', 'tags__name')
            search_query = SearchQuery(query, search_type='websearch')
            search_rank = SearchRank(search_vector, search_query)
            results = models.Material.objects.annotate(rank=search_rank).order_by('-rank').distinct()
    return render(request,
                  'matman/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


class SchemeListView(ListView):
    model = models.Scheme
    template_name_suffix = '_list'
    fields = ['name', 'prefix', 'numlen', 'postfix', 'is_active']
    paginate_by = 50


class SchemeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Scheme
    template_name_suffix = '_create'
    form_class = forms.SchemeCreateForm
    success_url = reverse_lazy('list-schemes')

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully created scheme <a href="{url}" class="alert-link">{self.object}</a>'


class SchemeEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Scheme
    template_name_suffix = '_edit'
    form_class = forms.SchemeEditForm
    success_url = reverse_lazy('list-schemes')

    def get_success_message(self, cleaned_data):
        url = self.object.get_absolute_url()
        return f'Successfully updated scheme <a href="{url}" class="alert-link">{self.object}</a>'


class SettingsView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.UserProfile
    form_class = forms.SettingsForm
    template_name_suffix = '_edit'
    success_message = 'Profile settings updated successfully'

    def get_success_url(self):
        return reverse_lazy('profile-settings')

    def get_object(self, queryset=None):
        return self.request.user.profile
