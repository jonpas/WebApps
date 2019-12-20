from django import forms

from . import models


class TaskCreateForm(forms.ModelForm):
    deadline = forms.SplitDateTimeField(label="Deadline", widget=forms.SplitDateTimeWidget())

    class Meta:
        model = models.Task
        fields = '__all__'
