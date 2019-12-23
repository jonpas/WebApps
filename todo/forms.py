from django import forms

from flatpickr import DateTimePickerInput

from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ['completed']
        widgets = {
            'deadline': DateTimePickerInput(),
        }
