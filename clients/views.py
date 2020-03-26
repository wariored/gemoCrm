from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, ListView, DetailView

from clients.forms import HackerForm, StartupForm
from clients.models import Hacker, Startup
from gemoCrm.utils.pagination_handler import get_pagination_data


def client_index(request):
    return render(request, 'clients/client_index.html')


# hacker section

@method_decorator(login_required, name='dispatch')
class CreateHackerView(CreateView):
    template_name = "clients/hackers/create_hacker.html"
    form_class = HackerForm
    success_url = reverse_lazy('clients:client-index')


@method_decorator(login_required, name='dispatch')
class HackerUpdateView(UpdateView):
    model = Hacker
    template_name = "clients/hackers/update_hacker.html"
    form_class = HackerForm
    success_url = reverse_lazy('clients:client-index')


@method_decorator(login_required, name='dispatch')
class HackerListView(ListView):
    model = Hacker
    template_name = 'clients/hackers/list_hacker.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(HackerListView, self).get_context_data(**kwargs)
        hackers = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(hackers, self.paginate_by)
        context['hackers'] = get_pagination_data(paginator, page)
        return context


@method_decorator(login_required, name='dispatch')
class HackerDetailView(DetailView):
    model = Hacker
    template_name = 'clients/hackers/detail_hacker.html'


# startup section

@method_decorator(login_required, name='dispatch')
class StartupCreateView(CreateView):
    template_name = "clients/startups/create_startup.html"
    form_class = StartupForm
    success_url = reverse_lazy('clients:client-index')


@method_decorator(login_required, name='dispatch')
class StartupUpdateView(UpdateView):
    model = Startup
    template_name = "clients/startups/update_startup.html"
    form_class = StartupForm
    success_url = reverse_lazy('clients:client-index')


@method_decorator(login_required, name='dispatch')
class StartupListView(ListView):
    model = Startup
    template_name = 'clients/startups/list_startup.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(StartupListView, self).get_context_data(**kwargs)
        startups = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(startups, self.paginate_by)
        context['startups'] = get_pagination_data(paginator, page)
        return context


@method_decorator(login_required, name='dispatch')
class StartupDetailView(DetailView):
    model = Startup
    template_name = 'clients/startups/detail_startup.html'
