from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class List(models.Model):
    name = models.CharField(max_length=60)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    reminder_before_deadline = models.DurationField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name
