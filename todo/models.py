from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=100, default='black')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.color})"


class List(models.Model):
    name = models.CharField(max_length=60)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.tags.all()})"


class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    reminder_days = models.IntegerField(default='0')
    reminder_hours = models.IntegerField(default='0')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.completed}, {self.deadline}, {self.reminder_before_deadline}, {self.tags.all()})"

    def reminder(self):
        time_to_deadline = self.deadline - timezone.now()
        time_to_deadline = max(0, time_to_deadline.days * 24 + time_to_deadline.seconds // 3600)
        reminder_time = max(0, self.reminder_days) * 24 + max(0, self.reminder_hours)
        return time_to_deadline < reminder_time

    def remind(self):
        return not self.completed and self.reminder()
