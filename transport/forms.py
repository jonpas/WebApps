from django import forms

from flatpickr import DateTimePickerInput

from . import models


class TransportForm(forms.ModelForm):
    class Meta:
        model = models.Transport
        exclude = ['carrier', 'passengers', 'passengers_confirmed', 'passengers_picked', 'attendees_rated']
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


class TransportRateForm(forms.ModelForm):
    class Meta:
        model = models.Transport
        fields = []

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super().__init__(*args, **kwargs)

    RATING_CHOICES = [
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    ]

    social = forms.ChoiceField(choices=RATING_CHOICES)
    on_time = forms.ChoiceField(choices=RATING_CHOICES)
    luggage = forms.ChoiceField(choices=RATING_CHOICES)
