from django.apps import AppConfig


class DoodleConfig(AppConfig):
    name = 'doodle'

    def ready(self):
        from . import models

        # Clear "temporary" users field on room as all websockets were closed (server offline)
        for model in models.Room.objects.all():
            model.users.clear()
