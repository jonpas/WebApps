from django.apps import AppConfig

import sys


class LudoConfig(AppConfig):
    name = 'ludo'

    def ready(self):
        ignore_args = ['makemigrations', 'migrate']
        if not [x for x in ignore_args if x in sys.argv]:
            from . import models

            # Clear "temporary" fields on room as all websockets were closed (server offline)
            for room in models.Room.objects.all():
                room.users.clear()

            # TODO models.Game.objects.all().delete()
