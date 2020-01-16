from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import F
from django.contrib.auth.models import User

import json
import random

from . import models

MIN_CLIENTS = 1
MAX_CLIENTS = 4
TIMEOUT = 180  # Seconds

# DEBUG
ROLL_6 = False


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.user = self.scope['user']

        self.room_group_name = f'ludo_{self.room_id}'
        self.room_owner_group_name = f'ludo_{self.room_id}_owner'
        self.room_user_group_stub = f'ludo_{self.room_id}_user_'

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
            # or automatically start game if max clients connected
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
                self.turn_game(timeout=True)
        else:
            # Notify owner if game not ready to start (not enough clients connected)
            user_count = room_model.users.count()
            if user_count < MIN_CLIENTS:
                self.send_owner(self.msg_game_ready(ready=False))

    # Receive message from WebSocket
    def receive(self, text_data):
        data_json = json.loads(text_data)
        msgtype = data_json['type']

        if msgtype == 'game_start':
            self.start_game()

        elif msgtype == 'game_roll':
            self.roll_game()

        elif msgtype == 'game_turn':
            self.turn_game(token=data_json['token'])

        elif msgtype == 'game_timeout':
            self.send_all(self.msg_game_timeout())
            self.turn_game(timeout=True)

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
        players = room_model.users.all()
        total_players = len(players)

        # Initialize board JSON
        state = {
            'bases': {
                'blue': ['blue-1', 'blue-2', 'blue-3', 'blue-4'],
                'red': ['red-1', 'red-2', 'red-3', 'red-4'] if total_players > 1 else [None] * 4,
                'green': ['green-1', 'green-2', 'green-3', 'green-4'] if total_players > 2 else [None] * 4,
                'yellow': ['yellow-1', 'yellow-2', 'yellow-3', 'yellow-4'] if total_players > 3 else [None] * 4
            },
            'homes': {
                'blue': [None] * 4,
                'red': [None] * 4,
                'green': [None] * 4,
                'yellow': [None] * 4
            },
            'fields': [None] * 40
        }

        # Initialize game
        room_model.game = models.Game.objects.create(
            state=state,
            rolls={}
        )
        room_model.game.players.set(players)
        room_model.save()

        # Send game start to all and unready to owner
        self.send_all(self.msg_game_start())
        self.send_owner(self.msg_game_ready(ready=False))

    def roll_game(self):
        roll = random.randint(1, 6) if not ROLL_6 else 6

        room_model = self.get_room_model()
        room_model.game.rolls[f'{self.user.id}'] = roll
        room_model.game.save()

        self.send_all(self.msg_game_roll(roll=roll))

        # Check if pre-turn
        # Everyone throws once, highest starts (last highest if multiple) if pre-turn
        rolls = room_model.game.rolls
        if len(rolls) == room_model.game.players.count():
            # Start first turn if all rolled or get available actions and continue turn
            if not room_model.game.player:
                # Set highest roller as first player
                max_id = int(max(rolls, key=rolls.get))
                room_model.game.player = User.objects.get(id=max_id)
                room_model.game.save()

                # Can only roll in pre-turn
                self.send_all(self.msg_game_turn(['roll']))
            else:
                actions = room_model.game.available_actions()
                if not actions:
                    # No actions available, move to next player
                    self.turn_game()
                else:
                    self.send_all(self.msg_game_turn(actions))

    def turn_game(self, token=None, timeout=False):
        room_model = self.get_room_model()

        knock = False
        if not timeout:
            # Apply move
            knock = room_model.game.move(token)
            room_model.game.save()

        # Check if player finished the game
        total_players = room_model.game.players.count()
        current_players = total_players - room_model.game.players_played.count()
        player = room_model.game.player
        color = room_model.game.color()

        if color and None not in room_model.game.state['homes'][color]:
            # Update statistics and message everyone about player finishing
            if current_players >= total_players:
                models.Profile.objects.filter(user=player.id).update(
                    first=F('first') + 1
                )
                self.send_all(self.msg_game_player_finish(player=player, position=1))
            elif current_players >= total_players - 1:
                models.Profile.objects.filter(user=player.id).update(
                    second=F('second') + 1
                )
                self.send_all(self.msg_game_player_finish(player=player, position=2))
            elif current_players >= total_players - 2:
                models.Profile.objects.filter(user=player.id).update(
                    third=F('third') + 1
                )
                self.send_all(self.msg_game_player_finish(player=player, position=3))
            elif current_players >= total_players - 3:
                models.Profile.objects.filter(user=player.id).update(
                    fourth=F('fourth') + 1
                )
                self.send_all(self.msg_game_player_finish(player=player, position=4))

            room_model.game.players_played.add(player)

        # Continue to next turn if players still playing or end game if all finished
        if room_model.game.players_played.count() < total_players:
            # Set next player or allow another roll/turn on 6
            if room_model.game.rolls.get(f'{self.user.id}', 0) != 6:
                # Find next player in players field and not in played list
                remaining_players = [x for x in room_model.game.players.all()
                                     if x not in room_model.game.players_played.all()]

                player_index = remaining_players.index(player) if player in remaining_players else 0
                new_player = remaining_players[0]
                if player_index + 1 < len(remaining_players):
                    new_player = remaining_players[player_index + 1]

                room_model.game.player = new_player
                room_model.game.save()

            # Always start turn with a roll
            self.send_all(self.msg_game_turn(actions=['roll'], knock=knock))
        else:
            self.end_game()

    def end_game(self):
        # Send end game message with state (before cleanup!)
        self.send_all(self.msg_game_end())

        # Cleanup
        room_model = self.get_room_model()
        room_model.game.delete()

        # Start new game if enough clients present or mark readiness for owner
        user_count = room_model.users.count()
        if user_count >= MAX_CLIENTS:
            self.start_game()
        elif user_count >= MIN_CLIENTS:
            self.send_owner(self.msg_game_ready(ready=True))
        else:
            self.send_owner(self.msg_game_ready(ready=False))

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
    def msg_game_ready(self, ready):
        return {
            'type': 'game_ready',
            'ready': ready
        }

    def msg_game_start(self):
        room_model = self.get_room_model()

        return {
            'type': 'game_start',
            'actions': ['roll'],
            'state': room_model.game.state,
            'timeout': TIMEOUT
        }

    def msg_game_roll(self, roll):
        return {
            'type': 'game_roll',
            'player': {
                'id': self.user.id,
                'name': self.user.get_username()
            },
            'roll': roll
        }

    def msg_game_turn(self, actions, knock=False):
        room_model = self.get_room_model()

        return {
            'type': 'game_turn',
            'actions': actions,
            'state': room_model.game.state,
            'player': {
                'id': room_model.game.player.id,
                'name': room_model.game.player.get_username()
            },
            'knock': knock,
            'timeout': TIMEOUT
        }

    def msg_game_player_finish(self, player, position):
        return {
            'type': 'game_player_finish',
            'finisher': {
                'id': player.id,
                'name': player.get_username()
            },
            'position': position
        }

    def msg_game_end(self):
        room_model = self.get_room_model()

        return {
            'type': 'game_end',
            'state': room_model.game.state
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
    def game_ready(self, event):
        self.send(text_data=json.dumps(event))

    def game_start(self, event):
        self.send(text_data=json.dumps(event))

    def game_roll(self, event):
        is_player = event['player']['id'] == self.user.id

        self.send(text_data=json.dumps({
            'type': event['type'],
            'player': event['player'],
            'roll': event['roll'],
            'rolled': is_player
        }))

    def game_turn(self, event):
        is_player = event['player']['id'] == self.user.id

        self.send(text_data=json.dumps({
            'type': event['type'],
            'actions': event['actions'] if is_player else [],
            'state': event['state'],
            'player': event['player'],
            'knock': event['knock'],
            'timeout': event['timeout']
        }))

    def game_player_finish(self, event):
        self.send(text_data=json.dumps(event))

    def game_end(self, event):
        self.send(text_data=json.dumps(event))

    def game_timeout(self, event):
        self.send(text_data=json.dumps(event))
