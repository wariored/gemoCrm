from django.forms import ModelForm

from sales.models import Contact, Deal


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class DealForm(ModelForm):
    class Meta:
        model = Deal
        exclude = ['created_at']
