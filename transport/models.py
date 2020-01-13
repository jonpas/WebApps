from django.db import models
from django.contrib.auth.models import User


class Transport(models.Model):
    carrier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_carrier')
    passengers = models.ManyToManyField(User, blank=True, related_name='transport_passenger')

    def __str__(self):
        return self.carrier.get_username()

    def __repr__(self):
        return f'Transport [{self.id}]: {self.carrier} ({self.passengers.all()})'
