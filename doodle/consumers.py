from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json

from . import models

MIN_CLIENTS = 2  # 3
MAX_CLIENTS = 8


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope['user']

        self.room_group_name = f'doodle_{self.room_id}'
        self.room_owner_group_name = f'doodle_{self.room_id}_owner'
        self.room_user_group_stub = f'doodle_{self.room_id}_user_'

        self.room_model = models.Room.objects.get(id=self.room_id)

        # Only connect if room not full
        if self.room_model.users.count() < MAX_CLIENTS:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.room_model.users.add(self.user)

            # Join single-user owner group
            if self.room_model.owner.id == self.user.id:
                async_to_sync(self.channel_layer.group_add)(
                    self.room_owner_group_name,
                    self.channel_name
                )

            # Join single-user user group
            async_to_sync(self.channel_layer.group_add)(
                f'{self.room_user_group_stub}_{self.user.id}',
                self.channel_name
            )

            self.accept()

            # Notify room about new user
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_connect',
                    'message': {
                        'id': self.user.id,
                        'name': self.user.username
                    }
                }
            )

            # Notify owner if game ready to start (enough clients connected)
            if self.room_model.users.count() >= MIN_CLIENTS:
                async_to_sync(self.channel_layer.group_send)(
                    self.room_owner_group_name,
                    {
                        'type': 'game_ready',
                        'message': True
                    }
                )

            # TODO Start game room is full
            if self.room_model.users.count() >= MAX_CLIENTS:
                print('TODO: full lobby - start game')
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.room_model.users.remove(self.user)

        # Notify room about leaving user
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_disconnect',
                'message': self.user.id
            }
        )

        # Notify owner if game not ready to start (not enough clients connected)
        if self.room_model.users.count() < MIN_CLIENTS:
            async_to_sync(self.channel_layer.group_send)(
                self.room_owner_group_name,
                {
                    'type': 'game_ready',
                    'message': False
                }
            )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text_data_json['sender'] = {
            'id': self.user.id,
            'name': self.user.username
        }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data_json
        )


    # Message handlers

    # Chat
    def chat(self, event):
        event['message'] = f'[{event["sender"]["name"]}] {event["message"]}'
        self.send(text_data=json.dumps(event))

    def user_connect(self, event):
        self.send(text_data=json.dumps(event))

    def user_disconnect(self, event):
        self.send(text_data=json.dumps(event))

    # Drawing
    def draw(self, event):
        self.send(text_data=json.dumps(event))

    # Game
    def game_ready(self, event):
        self.send(text_data=json.dumps(event))

    def game_start(self, event):
        self.send(text_data=json.dumps(event))
