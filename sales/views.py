from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from sales.forms import ContactForm, DealForm
from sales.models import Contact, Deal, DealType, DealStage


# contact section
from sales.utils.query_helper import get_deal_filters


@method_decorator(login_required, name='dispatch')
class ContactCreateView(CreateView):
    form_class = ContactForm
    template_name = 'sales/contacts/create_contact.html'

    def get_success_url(self):
        return reverse_lazy('sales:list-contact')


@method_decorator(login_required, name='dispatch')
class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'sales/contacts/update_contact.html'

    def get_success_url(self):
        return reverse_lazy('sales:list-contact')


@method_decorator(login_required, name='dispatch')
class ContactDetailView(DetailView):
    model = Contact
    template_name = 'sales/contacts/detail_contact.html'


@method_decorator(login_required, name='dispatch')
class ContactListView(ListView):
    model = Contact
    template_name = 'sales/sales_index.html'
    context_object_name = 'contacts'
    template_params = {}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        search_text = self.request.GET.get('search-text')
        if search_text:
            search_query = Q(first_name__icontains=search_text) | Q(last_name__icontains=search_text) \
                           | Q(email__icontains=search_text) | Q(startup__name__icontains=search_text)
            queryset = queryset.filter(search_query)
            self.template_params['search_text'] = search_text
        else:
            self.template_params['search_text'] = ""

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template_params"] = self.template_params

        return context


# deal section

@method_decorator(login_required, name='dispatch')
class DealCreateView(CreateView):
    form_class = DealForm
    template_name = 'sales/deals/create_deal.html'

    def get_success_url(self):
        return reverse_lazy('sales:list-deal')


@method_decorator(login_required, name='dispatch')
class DealUpdateView(UpdateView):
    model = Deal
    form_class = DealForm
    template_name = 'sales/deals/update_deal.html'

    def get_success_url(self):
        return reverse_lazy('sales:list-deal')


@method_decorator(login_required, name='dispatch')
class DealDetailView(DetailView):
    model = Deal
    template_name = 'sales/deals/detail_deal.html'


@method_decorator(login_required, name='dispatch')
class DealListView(ListView):
    model = Deal
    template_name = 'sales/sales_index.html'
    context_object_name = 'deals'
    filter_params = {}

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        query, self.filter_params = get_deal_filters(self.request, self.filter_params)
        if query is not None:
            queryset = queryset.filter(query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_params"] = self.filter_params
        context["deal_stages"] = DealStage.objects.all()
        context["deal_types"] = DealType.objects.all()
        context["filter_params"] = self.filter_params

        return context



