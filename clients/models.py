from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Client(models.Model):
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", blank=True, null=True,
                             on_delete=models.PROTECT)
    email = models.EmailField()
    city = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True)
    about = models.TextField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True


class Startup(Client):
    KIND_CHOICES = (
        ("L", "LEAD"),
        ("HL", "HOT LEAD"),
        ("C", "CLIENT")
    )
    name = models.CharField(max_length=250)
    kind = models.CharField(max_length=250, choices=KIND_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('clients:detail-startup', kwargs={'pk': self.pk})


class Hacker(Client):
    FIT_CHOICES = (
        ("P", "POTENTIAL FIT"),
        ("W", "WATCH LIST"),
        ("N", "NOT A FIT")
    )

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    fit = models.CharField(max_length=30, choices=FIT_CHOICES, null=True, blank=True)
    startup = models.ForeignKey(Startup, related_name="hackers", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name}{self.last_name}".replace(" ", "")

    def get_absolute_url(self):
        return reverse('clients:detail-hacker', kwargs={'pk': self.pk})


class JobPosition(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    external_id = models.BigIntegerField()

    def __str__(self):
        return f"{self.external_id} {self.name}"


class JobApplication(models.Model):
    external_id = models.BigIntegerField()
    status = models.CharField(max_length=30)
    source = models.CharField(max_length=250, null=True, blank=True)
    rejection_reason = models.CharField(max_length=250, null=True, blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    hacker = models.ForeignKey(Hacker, related_name="job_applications", on_delete=models.CASCADE,
                               null=True, blank=True)
    positions = models.ManyToManyField(JobPosition, related_name="job_applications", blank=True)

    def __str__(self):
        return f"{self.external_id} {self.status} {self.hacker}"
