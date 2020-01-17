# Generated by Django 3.0.2 on 2020-01-17 11:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transport', '0014_auto_20200117_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='attendees_rated',
            field=models.ManyToManyField(blank=True, related_name='transport_attendee_rated', to=settings.AUTH_USER_MODEL),
        ),
    ]
