# Generated by Django 3.0.2 on 2020-01-09 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doodle', '0006_auto_20200109_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='live',
        ),
    ]
