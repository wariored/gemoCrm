from django.contrib.auth.models import User
from django.db import models


class Client(models.Model):
    user = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", blank=True, null=True,
                             on_delete=models.PROTECT)
    email = models.EmailField()
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    about = models.TextField(max_length=250, null=True, blank=True)

    class Meta:
        abstract = True


class Startup(Client):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Hacker(Client):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
