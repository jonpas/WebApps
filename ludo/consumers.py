from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json

from . import models

MIN_CLIENTS = 2
REQ_CLIENTS = 4
TIMEOUT = 60  # Seconds


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope['user']

        self.room_group_name = f'ludo_{self.room_id}'
        self.room_user_group_stub = f'ludo_{self.room_id}_user_'

        # Only connect if room not full
        room_model = self.get_room_model()
        if room_model.users.count() < REQ_CLIENTS:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            room_model.users.add(self.user)

            # Join single-user user group
            async_to_sync(self.channel_layer.group_add)(
                f'{self.room_user_group_stub}_{self.user.id}',
                self.channel_name
            )

            self.accept()

            # Notify room about new user
            self.send_all(self.msg_user_connect())

            # Start new game if enough clients connected
            user_count = room_model.users.count()
            if user_count >= REQ_CLIENTS:
                self.start_game()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        room_model = self.get_room_model()
        room_model.users.remove(self.user)

        # Notify room about leaving user
        self.send_all(self.msg_user_disconnect())

        # Move to next player if current one disconnected (disqualify)
        # user_count = room_model.users.count()
        # if room_model.game:
        #     if user_count < MIN_CLIENTS:
        #         self.end_game()
        #     elif room_model.game.player.id == self.user.id:
        #         self.next_game(timeout=True)

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        msgtype = data_json['type']

        # TODO

        if msgtype == 'game_start':
            self.start_game()

        elif msgtype == 'game_timeout':
            self.send_all(self.msg_game_timeout())
            self.next_game(timeout=True)

    # Send target helpers
    def send_all(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            data
        )

    def send_user(self, id, data):
        async_to_sync(self.channel_layer.group_send)(
            f'{self.room_user_group_stub}_{id}',
            data
        )

    # Database helpers
    def get_room_model(self):
        return models.Room.objects.get(id=self.room_id)

    # Game control
    def start_game(self, player=None):
        # TODO
        # Send game start to all
        self.send_all(self.msg_game_start())

    def next_game(self, guessed=False, timeout=False):
        # TODO
        if not timeout:
            self.send_all(self.msg_game_next(guessed))

        self.end_game()

    def end_game(self):
        # TODO
        room_model = self.get_room_model()

        self.send_all(self.msg_game_end())

        # Start new game if enough clients present
        user_count = room_model.users.count()
        if user_count >= REQ_CLIENTS:
            self.start_game()

    # Server message creators
    def msg_user_connect(self):
        return {
            'type': 'user_connect',
            'id': self.user.id,
            'name': self.user.get_username()
        }

    def msg_user_disconnect(self):
        return {
            'type': 'user_disconnect',
            'id': self.user.id,
            'name': self.user.get_username()
        }

    # Game
    def msg_game_start(self):
        # room_model = self.get_room_model()

        return {
            'type': 'game_start',
            'player': {
                'id': 0,  # TODO room_model.game.player.id
                'name': ''  # TODO room_model.game.player.get_username()
            },
            'timeout': TIMEOUT
        }

    def msg_game_next(self, winner):
        return {
            'type': 'game_next',
            'winner': {
                'id': self.user.id,
                'name': self.user.get_username()
            }
        }

    def msg_game_end(self):
        return {
            'type': 'game_end'
        }

    def msg_game_timeout(self):
        return {
            'type': 'game_timeout',
            'player': {
                'id': self.user.id,
                'name': self.user.get_username()
            }
        }

    # Client message handlers
    def user_connect(self, event):
        self.send(text_data=json.dumps(event))

    def user_disconnect(self, event):
        self.send(text_data=json.dumps(event))

    # Game
    def game_start(self, event):
        self.send(text_data=json.dumps(event))

    def game_next(self, event):
        self.send(text_data=json.dumps(event))

    def game_end(self, event):
        self.send(text_data=json.dumps(event))

    def game_timeout(self, event):
        self.send(text_data=json.dumps(event))
