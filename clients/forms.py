from django.forms import ModelForm

from clients.models import Hacker, Startup


class HackerForm(ModelForm):
    class Meta:
        model = Hacker
        fields = ['email', 'city', 'country', 'postal_code', 'address', 'about', 'first_name', 'last_name', 'fit',
                  'startup']


class StartupForm(ModelForm):
    class Meta:
        model = Startup
        fields = ['email', 'city', 'country', 'postal_code', 'address', 'about', 'name', 'kind']
