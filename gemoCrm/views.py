from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View

from gemoCrm.utils.user_helper import authenticate_user


@login_required
def index(request):
    return render(request, 'gemoCrm/index.html')


class LoginView(View):
    template_name = 'gemoCrm/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate_user(email, password)
        context = {}

        if user is not None:
            if user.is_active:
                login(request, user)

                return redirect(self.request.GET.get('next', '/'))
            else:
                context['error_message'] = "user is not active"
        else:
            context['error_message'] = "email or password not correct"

        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(settings.LOGIN_URL)
