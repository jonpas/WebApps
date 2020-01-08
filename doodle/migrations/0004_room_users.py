# Generated by Django 3.0.2 on 2020-01-08 15:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doodle', '0003_auto_20200107_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
