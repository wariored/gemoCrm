from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView

from clients.models import Exchange
from gemoCrm.forms import UserProfileForm
from gemoCrm.models import Role
from gemoCrm.utils.search_helper import get_search_result_reverse
from gemoCrm.utils.user_helper import authenticate_user


@login_required
def index(request):
    users = User.objects.all()
    talent_acquisitions = users.filter(profile__roles=Role.TALENT_ACQUISITION).values()
    sales = users.filter(profile__roles=Role.SALES).values()

    for talent_acquisition in talent_acquisitions:
        exchanges_count = Exchange.objects.filter(
            Q(from_email=talent_acquisition["email"]) | Q(to_email=talent_acquisition["email"])).count()
        talent_acquisition["touch_point"] = exchanges_count

    for sale in sales:
        exchanges_count = Exchange.objects.filter(
            Q(from_email=sale["email"]) | Q(to_email=sale["email"])).count()
        sale["touch_point"] = exchanges_count

    context = {
        'talent_acquisitions': talent_acquisitions,
        'sales': sales
    }
    return render(request, 'gemoCrm/index.html', context)


class LoginView(View):
    template_name = 'gemoCrm/login.html'

    def get(self, request):
        next_url = request.GET.get('next', '')
        context = {
            'next_url': next_url
        }
        return render(request, self.template_name, context)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate_user(email, password)
        context = {}

        if user is not None:
            if user.is_active:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect(request.GET.get('next', '/'))
            else:
                context['error_message'] = "user is not active"
        else:
            context['error_message'] = "email or password not correct"

        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "gemoCrm/update_profile.html"

    def get_success_url(self):
        self.request.session['profile_update'] = 'updated'
        return reverse_lazy('update-profile', kwargs={'pk': self.object.id})


class GeneralSearchView(View):
    def post(self, request):
        search_value = request.POST['search']
        reverse_search = get_search_result_reverse(search_value)
        if reverse_search is None:
            return HttpResponseNotFound("Nothing was found")
        return redirect(reverse_search)
