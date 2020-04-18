from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from clients.models import Startup
from gemoCrm.utils.media_helper import get_deal_file_path, get_contact_file_path


class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    startup = models.ForeignKey(Startup, related_name='contacts', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse('sales:update-contact', kwargs={'pk': self.pk})


class ContactFile(models.Model):
    contact = models.ForeignKey(Contact, related_name='contact_files', on_delete=models.CASCADE)
    media = models.FileField(upload_to=get_contact_file_path)

    def __str__(self):
        return f"{self.pk}-{self.contact.email}"


class ContactLifecycle(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


class DealFile(models.Model):
    deal = models.ForeignKey(Deal, related_name='deal_files', on_delete=models.CASCADE)
    media = models.FileField(upload_to=get_deal_file_path)

    def __str__(self):
        return f"{self.pk}-{self.deal.name}"


class Note(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(max_length=2000)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class ContactNote(Note):
    contact = models.ForeignKey(Contact, related_name='contact_notes', on_delete=models.CASCADE)


class DealNote(Note):
    deal = models.ForeignKey(Deal, related_name='deal_notes', on_delete=models.CASCADE)


class Ticket(models.Model):
    contact = models.ForeignKey(Contact, related_name='contact_tickets', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True,
                                    blank=True)
    created_by = models.ForeignKey(User, related_name='created_tickets', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.pk}-{self.contact.email}'
