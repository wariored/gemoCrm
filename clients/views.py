from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, CreateView, ListView, DetailView

from clients.forms import HackerForm, StartupForm
from clients.models import Hacker, Startup, JobPosition, JobApplication, Exchange
from clients.utils.client_helper import store_hackers_data
from gemoCrm.utils.pagination_handler import get_pagination_data


@login_required
def client_index(request):
    page = request.GET.get('page')
    client_type = request.GET.get('client-type')
    search_text = request.GET.get('search-text', '')
    paginate_by = 15

    if client_type == "hackers":
        hackers = Hacker.objects.all()
        if search_text:
            hackers = hackers.filter(Q(email__icontains=search_text) | Q(first_name__icontains=search_text) | Q(
                last_name__icontains=search_text))
        paginator = Paginator(hackers, paginate_by)
        client_count = Hacker.objects.count()

    else:
        startups = Startup.objects.all()
        if search_text:
            startups = startups.filter(
                Q(email__icontains=search_text) | Q(name__icontains=search_text) | Q(country__icontains=search_text))
        paginator = Paginator(startups, paginate_by)
        client_type = "startups"
        client_count = Startup.objects.count()

    pagination_values = get_pagination_data(paginator, page)

    context = {
        'client_type': client_type,
        'paginator': paginator,
        'client_count': client_count,
        'search_text': search_text,
        client_type: pagination_values
    }

    return render(request, 'clients/client_index.html', context)


@login_required
def import_from_greenhouse(request):
    store_hackers_data()
    return HttpResponse("done")


# hacker section

@method_decorator(login_required, name='dispatch')
class CreateHackerView(CreateView):
    template_name = "clients/hackers/create_hacker.html"
    form_class = HackerForm

    def get_success_url(self):
        return reverse_lazy('clients:detail-hacker', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class HackerUpdateView(UpdateView):
    model = Hacker
    template_name = "clients/hackers/update_hacker.html"
    form_class = HackerForm

    def get_success_url(self):
        return reverse_lazy('clients:detail-hacker', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class HackerListView(ListView):
    model = Hacker
    template_name = 'clients/hackers/list_hacker.html'
    paginate_by = 20

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        position_id = self.request.GET.get('position')
        if position_id:
            queryset = queryset.filter(job_applications__positions__id=position_id).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(HackerListView, self).get_context_data(**kwargs)
        hackers = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(hackers, self.paginate_by)

        position_id = self.request.GET.get('position')
        if position_id:
            context['additional_params'] = f"&position={position_id}"
            context['position'] = JobPosition.objects.get(pk=position_id)

        context['hackers'] = get_pagination_data(paginator, page)
        return context


@method_decorator(login_required, name='dispatch')
class HackerDetailView(DetailView):
    model = Hacker
    template_name = 'clients/hackers/detail_hacker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hacker = self.get_object()
        exchanges = Exchange.objects.filter(Q(from_email=hacker.email) | Q(to_email=hacker.email))
        context['exchanges'] = exchanges
        return context


# startup section

@method_decorator(login_required, name='dispatch')
class StartupCreateView(CreateView):
    template_name = "clients/startups/create_startup.html"
    form_class = StartupForm

    def get_success_url(self):
        return reverse_lazy('clients:detail-startup', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class StartupUpdateView(UpdateView):
    model = Startup
    template_name = "clients/startups/update_startup.html"
    form_class = StartupForm

    def get_success_url(self):
        return reverse_lazy('clients:detail-startup', kwargs={'pk': self.object.id})


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startup = self.get_object()
        exchanges = Exchange.objects.filter(Q(from_email=startup.email) | Q(to_email=startup.email))
        context['exchanges'] = exchanges
        return context


# job section

@login_required
def client_jobs_index(request):
    job_type = request.GET.get('job-type', "applications")
    job_count = None
    chart_values = {}
    if job_type == "applications":
        job_count = JobApplication.objects.count()
        job_applications_grouped_by_status = JobApplication.objects.values('status').annotate(
            count=Count('status')).order_by()
        chart_pie_labels = [group['status'] for group in job_applications_grouped_by_status]
        chart_pie_data = [group['count'] for group in job_applications_grouped_by_status]

        job_applications_grouped_by_applied_date = JobApplication.objects.annotate(
            month=TruncMonth('applied_at')).values(
            'month').annotate(c=Count('id')).order_by('month')
        chart_applications_line_x = [x["c"] for x in job_applications_grouped_by_applied_date]
        chart_applications_line_y = [str(y["month"].date()) for y in job_applications_grouped_by_applied_date]
        chart_values = {
            'chart_pie_labels': chart_pie_labels,
            'chart_pie_data': chart_pie_data,
            'chart_applications_line_x': chart_applications_line_x,
            'chart_applications_line_y': chart_applications_line_y
        }
    else:
        job_count = JobPosition.objects.count()

    context = {
        'job_type': job_type,
        'job_count': job_count,
        'chart_values': chart_values,
    }
    return render(request, 'clients/jobs/jobs_index.html', context)


@method_decorator(login_required, name='dispatch')
class JobPositionDetailView(DetailView):
    model = JobPosition
    template_name = 'clients/jobs/detail_job_position.html'
    context_object_name = 'job_position'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hackers_applied_count = Hacker.objects.filter(job_applications__positions=self.object).distinct().count()
        context['hackers_applied_count'] = hackers_applied_count
        return context


@method_decorator(login_required, name='dispatch')
class JobPositionListView(ListView):
    model = JobPosition
    template_name = 'clients/jobs/list_job_positions.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super(JobPositionListView, self).get_context_data(**kwargs)
        job_positions = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(job_positions, self.paginate_by)
        context['job_positions'] = get_pagination_data(paginator, page)
        return context


@method_decorator(login_required, name='dispatch')
class JobApplicationListView(ListView):
    model = JobApplication
    template_name = 'clients/jobs/list_job_applications.html'
    paginate_by = 8

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        position_id = self.request.GET.get('position')
        if position_id:
            queryset = queryset.filter(positions__id=position_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(JobApplicationListView, self).get_context_data(**kwargs)
        job_applications = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(job_applications, self.paginate_by)
        context['job_applications'] = get_pagination_data(paginator, page)

        position_id = self.request.GET.get('position')
        if position_id:
            context['additional_params'] = f"&position={position_id}"
            context['position'] = JobPosition.objects.get(pk=position_id)

        return context


@method_decorator(login_required, name='dispatch')
class JobApplicationDetailView(DetailView):
    model = JobApplication
    template_name = 'clients/jobs/detail_job_application.html'
    context_object_name = 'job_application'


# exchange section

@method_decorator(login_required, name='dispatch')
class ExchangeDetailView(DetailView):
    model = Exchange
    template_name = 'clients/exchanges/detail_exchange.html'


@method_decorator(login_required, name='dispatch')
class ExchangeListView(ListView):
    model = Exchange
    template_name = 'clients/exchanges/list_exchange.html'
    paginate_by = 8
    additional_params = ""
    result_filter = {}

    def get_queryset(self, *args, **kwargs):
        self.result_filter = {}
        queryset = super().get_queryset()
        from_email = self.request.GET.get('from-email')
        to_email = self.request.GET.get('to-email')
        from_date = self.request.GET.get('from-date')
        to_date = self.request.GET.get('to-date')
        message_contains = self.request.GET.get('message-contains')
        email_client = self.request.GET.get('email')
        email_member = self.request.GET.get('email-member')
        if from_email:
            queryset = queryset.filter(from_email=from_email)
            self.additional_params += f"&from-email={from_email}"
            self.result_filter["from"] = from_email
        if to_email:
            queryset = queryset.filter(to_email=to_email)
            self.additional_params += f"&to-email={to_email}"
            self.result_filter["to"] = to_email
        if from_date:
            queryset = queryset.filter(sent_date__gte=from_date)
            self.additional_params += f"&from-date={from_date}"
            self.result_filter["from_date"] = from_date
        if to_date:
            queryset = queryset.filter(sent_date__lte=to_date)
            self.additional_params += f"&to-date={to_date}"
            self.result_filter["to_date"] = to_date
        if message_contains:
            queryset = queryset.filter(message__icontains=message_contains)
            self.additional_params += f"&message-contains={message_contains}"
            self.result_filter["message_contains"] = message_contains
        if email_client:
            queryset = queryset.filter(Q(from_email=email_client) | Q(to_email=email_client))
        if email_member:
            queryset = queryset.filter(Q(from_email=email_member) | Q(to_email=email_member))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exchanges = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(exchanges, self.paginate_by)
        context['exchanges'] = get_pagination_data(paginator, page)

        client = self.request.GET.get('client')
        email_client = self.request.GET.get('email')
        email_member = self.request.GET.get('email-member')
        if email_client:
            self.additional_params += f"&email={email_client}"
            if client == "hacker":
                try:
                    hacker = Hacker.objects.get(email=email_client)
                except Hacker.DoesNotExist:
                    pass
                else:
                    self.additional_params += '&client=hacker'
                    context['hacker'] = hacker
            elif client == "startup":
                try:
                    startup = Startup.objects.get(email=email_client)
                except Startup.DoesNotExist:
                    pass
                else:
                    self.additional_params += '&client=startup'
                    context['startup'] = startup
        if email_member:
            self.additional_params += f"&email-member={email_member}"
        context['additional_params'] = self.additional_params
        context['result_filter'] = self.result_filter
        return context
