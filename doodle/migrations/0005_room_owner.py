# Generated by Django 3.0.2 on 2020-01-09 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('doodle', '0004_room_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
