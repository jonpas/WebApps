from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Room [{self.id}]: {self.name}"
