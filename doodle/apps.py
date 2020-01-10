from django.apps import AppConfig


class DoodleConfig(AppConfig):
    name = 'doodle'

    def ready(self):
        from . import models

        # Clear "temporary" fields on room as all websockets were closed (server offline)
        for room in models.Room.objects.all():
            room.users.clear()

        models.Game.objects.all().delete()
