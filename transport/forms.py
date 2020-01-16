from django import forms

from flatpickr import DateTimePickerInput

from . import models


class TransportForm(forms.ModelForm):
    class Meta:
        model = models.Transport
        exclude = ['carrier', 'passengers']
        widgets = {
            'departure_time': DateTimePickerInput(),
        }
