from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=100, blank=True)

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
    reminder_before_deadline = models.DurationField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} ({self.completed}, {self.deadline}, {self.reminder_before_deadline}, {self.tags.all()})"

    def time_to_deadline(self):
        return self.reminder_before_deadline

    def remind(self):
        return not self.completed and self.reminder_before_deadline is not None
