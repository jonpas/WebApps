from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

import json

from . import models


MAX_CLIENTS = 8


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'doodle_{self.room_id}'
        self.user = self.scope['user']
        self.room_model = models.Room.objects.get(id=self.room_id)

        # Only connect if room not full
        if self.room_model.users.count() < MAX_CLIENTS:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.room_model.users.add(self.user)

            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_add',
                    'message': {
                        'id': self.user.id,
                        'name': self.user.username
                    }
                }
            )

            self.accept()
        else:
            # TODO Handle on client
            self.reject()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.room_model.users.remove(self.user)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'user_remove',
                'message': self.user.id
            }
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            json.loads(text_data)
        )

    # Message handlers

    def chat(self, event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type': event['type'],
            'message': f'[{self.user.username}] {message}'
        }))

    def draw(self, event):
        self.send(text_data=json.dumps(event))

    def user_add(self, event):
        self.send(text_data=json.dumps(event))

    def user_remove(self, event):
        self.send(text_data=json.dumps(event))
