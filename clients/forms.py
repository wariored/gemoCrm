from django.forms import ModelForm

from clients.models import Hacker, Startup


class HackerForm(ModelForm):
    class Meta:
        model = Hacker
        exclude = ['user']


class StartupForm(ModelForm):
    class Meta:
        model = Startup
        exclude = ['user']
