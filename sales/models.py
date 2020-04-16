from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from clients.models import Startup


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    startup = models.ForeignKey(Startup, related_name='contacts', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('sales:update-contact', kwargs={'pk': self.pk})


class DealStage(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DealType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Deal(models.Model):
    name = models.CharField(max_length=250)
    deal_stage = models.ForeignKey(DealStage, related_name='stage_deals', on_delete=models.PROTECT)
    amount = models.IntegerField(blank=True, null=True)
    deal_type = models.ForeignKey(DealType, related_name='type_deals', on_delete=models.PROTECT, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='owner_deals', on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Startup, related_name='startup_deals', on_delete=models.SET_NULL, blank=True, null=True)
    contact = models.ForeignKey(Contact, related_name='contact_deals', on_delete=models.SET_NULL, blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sales:update-deal', kwargs={'pk': self.pk})
