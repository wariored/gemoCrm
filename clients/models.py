from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Client(models.Model):
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", blank=True, null=True,
                             on_delete=models.PROTECT)
    email = models.EmailField(unique=True)
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

    class Meta:
        ordering = ['name']

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

    class Meta:
        ordering = ['last_name']

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

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.external_id} {self.status} {self.hacker}"


class Exchange(models.Model):
    """
    The conversation exchange between clients and teams
    """
    HACKER_TYPE = "H"
    STARTUP_TYPE = "S"
    TEAM_MEMBER_TYPE = "T"
    EXCHANGE_ORIGIN_TYPE_CHOICES = (
        (HACKER_TYPE, "Hacker"),
        (STARTUP_TYPE, "Startup"),
        (TEAM_MEMBER_TYPE, "Team Member")
    )

    message = models.TextField()
    from_type = models.CharField(max_length=30, choices=EXCHANGE_ORIGIN_TYPE_CHOICES)
    to_type = models.CharField(max_length=30, choices=EXCHANGE_ORIGIN_TYPE_CHOICES)
    from_email = models.EmailField()
    to_email = models.EmailField()
    sent_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-sent_date']

    def __str__(self):
        return f"{self.pk}-{self.from_email}=>{self.to_email}"

    def _option(self, value):
        options = {
            self.HACKER_TYPE: Hacker.objects.get(email=self.from_email),
            self.STARTUP_TYPE: Startup.objects.get(email=self.from_email),
            self.TEAM_MEMBER_TYPE: User.objects.get(email=self.from_email)
        }
        return options[value]

    def get_from(self):
        return self._option(self.from_email)

    def get_to(self):
        return self._option(self.to_email)
