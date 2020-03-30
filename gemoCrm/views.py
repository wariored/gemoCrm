from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import View, UpdateView

from gemoCrm.forms import UserProfileForm
from gemoCrm.utils.user_helper import authenticate_user


@login_required
def index(request):
    return render(request, 'gemoCrm/index.html')


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
