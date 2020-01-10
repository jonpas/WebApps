from django.apps import AppConfig


class LudoConfig(AppConfig):
    name = 'ludo'

    def ready(self):
        from . import models

        # Clear "temporary" fields on room as all websockets were closed (server offline)
        for room in models.Room.objects.all():
            room.users.clear()

        # TODO models.Game.objects.all().delete()
