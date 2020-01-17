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


class TransportConfirmForm(forms.ModelForm):
    class Meta:
        model = models.Transport
        fields = ['passengers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['passengers'].queryset = models.Transport.objects.get(
                id=self.instance.id
            ).passengers.all()


class TransportDepartForm(forms.ModelForm):
    class Meta:
        model = models.Transport
        fields = ['passengers_confirmed']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['passengers_confirmed'].queryset = models.Transport.objects.get(
                id=self.instance.id
            ).passengers_confirmed.all()
