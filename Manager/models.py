from django.db import models

class WellKnownLocation(models.Model):
    location_name = models.CharField(max_length=300, unique=True)