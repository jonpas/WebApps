# Generated by Django 3.0.2 on 2020-01-14 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ludo', '0006_game_total_players'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='total_players',
            field=models.IntegerField(),
        ),
    ]
