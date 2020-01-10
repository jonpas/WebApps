from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import F
from django.utils import timezone

import json
import math

from . import models

MIN_CLIENTS = 2  # 3
MAX_CLIENTS = 8  # 8
TIMEOUT = 180  # Seconds
MAX_POINTS = 300


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope['user']

        self.room_group_name = f'doodle_{self.room_id}'
        self.room_owner_group_name = f'doodle_{self.room_id}_owner'
        self.room_user_group_stub = f'doodle_{self.room_id}_user_'

        # Only connect if room not full
        room_model = self.get_room_model()
        if room_model.users.count() < MAX_CLIENTS:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            room_model.users.add(self.user)

            # Join single-user owner group
            if room_model.owner.id == self.user.id:
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
            self.send_all(self.msg_user_connect())

            # Notify owner if game ready to start (enough clients connected)
            user_count = room_model.users.count()
            if user_count >= MAX_CLIENTS:
                self.start_game()
            elif user_count >= MIN_CLIENTS:
                self.send_owner(self.msg_game_ready(ready=True))
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
        user_count = room_model.users.count()
        if room_model.game:
            if user_count < MIN_CLIENTS:
                self.end_game()
            elif room_model.game.player.id == self.user.id:
                self.next_game(timeout=True)
        else:
            # Notify owner if game not ready to start (not enough clients connected)
            user_count = room_model.users.count()
            if user_count < MIN_CLIENTS:
                self.send_owner(self.msg_game_ready(ready=False))

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        msgtype = data_json['type']

        if msgtype == 'draw':
            self.send_all(self.msg_draw(data_json))

        elif msgtype == 'chat':
            # Send message to room group
            self.send_all(self.msg_chat(data_json["message"]))

            # Guessing if game is live
            room_model = self.get_room_model()
            if room_model.game and room_model.game.player.id != self.user.id:
                if data_json['message'] == room_model.game.word:
                    self.next_game(guessed=True)

        elif msgtype == 'game_start':
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

    def send_owner(self, data):
        async_to_sync(self.channel_layer.group_send)(
            self.room_owner_group_name,
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
        room_model = self.get_room_model()
        if player:
            # Update player (next round)
            room_model.game.player = player
            room_model.game.word = room_model.get_random_word()
            room_model.game.start_time = timezone.now()
            room_model.game.save()
        else:
            # Select random first player, word and initialize game
            room_model.game = models.Game.objects.create(
                player=player if player else room_model.get_random_user(),
                word=room_model.get_random_word()
            )
            room_model.save()

        # Send game start to all (with word to player) and unready on owner
        self.send_all(self.msg_game_start())
        self.send_owner(self.msg_game_ready(ready=False))

    def next_game(self, guessed=False, timeout=False):
        room_model = self.get_room_model()

        if not timeout:
            self.send_all(self.msg_game_next(guessed))

        if guessed:
            # Update statistics
            delta = timezone.now() - room_model.game.start_time
            elapsed = delta.total_seconds()

            # Winner gets points based on elapsed time
            winner_points = (TIMEOUT - elapsed) * (MAX_POINTS / TIMEOUT)
            # Player (drawer) gets half of winner's points
            player_points = winner_points / 2

            # Round up to nearest ten
            winner_points = int(math.ceil(winner_points / 10.0)) * 10
            player_points = int(math.ceil(player_points / 10.0)) * 10
            print(1, winner_points)
            print(2, player_points)

            # Add new points (winner is current user, player is drawer)
            models.Profile.objects.filter(id=self.user.id).update(
                wins=F('wins') + 1,
                points=F('points') + winner_points
            )
            models.Profile.objects.filter(id=room_model.game.player.id).update(
                played=F('played') + 1,
                points=F('points') + player_points
            )

        # Add player to played list
        room_model.game.players_played.add(room_model.game.player)

        # Find next player in users order field and not in played list
        remaining_players = [x for x in room_model.users.all() if x not in room_model.game.players_played.all()]

        # Start new game if any user has not yet played
        if remaining_players:
            self.start_game(player=remaining_players[0])
        else:
            self.end_game()

    def end_game(self):
        # Cleanup
        room_model = self.get_room_model()
        room_model.game.delete()

        self.send_all(self.msg_game_end())

        # Start new game or mark readiness for owner
        user_count = room_model.users.count()
        if user_count >= MAX_CLIENTS:
            self.start_game()
        elif user_count >= MIN_CLIENTS:
            self.send_owner(self.msg_game_ready(ready=True))
        else:
            self.send_owner(self.msg_game_ready(ready=False))

    # Server message creators
    # Chat
    def msg_chat(self, message):
        return {
            'type': 'chat',
            'message': message,
            'sender': {
                'id': self.user.id,
                'name': self.user.username
            }
        }

    def msg_user_connect(self):
        return {
            'type': 'user_connect',
            'id': self.user.id,
            'name': self.user.username
        }

    def msg_user_disconnect(self):
        return {
            'type': 'user_disconnect',
            'id': self.user.id,
            'name': self.user.username
        }

    # Drawing
    def msg_draw(self, data_json):
        return data_json

    # Game
    def msg_game_ready(self, ready):
        return {
            'type': 'game_ready',
            'ready': ready
        }

    def msg_game_start(self):
        room_model = self.get_room_model()

        return {
            'type': 'game_start',
            'word': room_model.game.word,
            'draw': False,
            'player': {
                'id': room_model.game.player.id,
                'name': room_model.game.player.username
            },
            'timeout': TIMEOUT
        }

    def msg_game_next(self, guessed):
        room_model = self.get_room_model()

        return {
            'type': 'game_next',
            'word': room_model.game.word,
            'guessed': guessed,
            'winner': {
                'id': self.user.id,
                'name': self.user.username
            } if guessed else None
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
                'name': self.user.username
            }
        }

    # Client message handlers
    # Chat
    def chat(self, event):
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
        is_player = event['player']['id'] == self.user.id

        self.send(text_data=json.dumps({
            'type': event['type'],
            'word': event['word'] if is_player else '',
            'draw': is_player,
            'player': event['player'],
            'timeout': event['timeout']
        }))

    def game_next(self, event):
        self.send(text_data=json.dumps(event))

    def game_end(self, event):
        self.send(text_data=json.dumps(event))

    def game_timeout(self, event):
        self.send(text_data=json.dumps(event))
