from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class AbeUser(AbstractUser):
    is_guest = models.BooleanField(default=False)


class Log(models.Model):
    date = models.DateField()
    state = models.IntegerField(default=0)
    location = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(AbeUser, on_delete=models.CASCADE)
    well_known_location = models.IntegerField(default=0)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "date"], name="log_unique"),
        ]
