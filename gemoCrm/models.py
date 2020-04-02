from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):
    """
    The Role entries are managed by the system,
    automatically created via a Django data migration.
    """
    TALENT_ACQUISITION = 1
    SALES = 2
    ACCOUNT_MANAGER = 3

    ROLE_CHOICES = (
        (TALENT_ACQUISITION, 'Talent Acquisition'),
        (SALES, 'Sales'),
        (ACCOUNT_MANAGER, 'Account Manager'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, related_name="user_profiles")

    def __str__(self):
        return f"{self.user}"
