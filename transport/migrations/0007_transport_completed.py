# Generated by Django 3.0.2 on 2020-01-16 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0006_auto_20200116_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='transport',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]