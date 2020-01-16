from django import db
import django_filters

from flatpickr import DateTimePickerInput

from . import models


class TransportFilter(django_filters.FilterSet):
    class Meta:
        model = models.Transport
        fields = {
            'departure_time': ['exact', 'lte', 'gte'],
            'departure_location': ['exact'],
            'arrival_location': ['exact'],
            'price': ['exact', 'lte', 'gte'],
        }
        filter_overrides = {
            db.models.DateTimeField: {
                'filter_class': django_filters.DateTimeFilter,
                'extra': lambda f: {
                    'widget': DateTimePickerInput,
                },
            },
        }
