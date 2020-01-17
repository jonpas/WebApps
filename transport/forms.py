from django import forms

from flatpickr import DateTimePickerInput

from . import models


class TransportForm(forms.ModelForm):
    class Meta:
        model = models.Transport
        exclude = ['carrier', 'passengers', 'passengers_confirmed', 'passengers_picked']
        widgets = {
            'departure_time': DateTimePickerInput(),
        }
