from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from jsonfield import JSONField

ENTRANCES = {'blue': 33 - 1, 'red': 3 - 1, 'green': 13 - 1, 'yellow': 23 - 1}


class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ludo_player')
    players = models.ManyToManyField(User, blank=True, related_name='ludo_players')
    players_played = models.ManyToManyField(User, blank=True, related_name='ludo_played')
    state = JSONField()
    rolls = JSONField()

    def __str__(self):
        return f'{self.state}'

    def __repr__(self):
        return f'Game [{self.id}]: {self.state} ({self.players.all()})'

    def color(self):
        players = self.players.all()
        total_players = len(players)

        if self.player == players[0]:
            return 'blue'
        elif total_players > 1 and self.player == players[1]:
            return 'red'
        elif total_players > 2 and self.player == players[2]:
            return 'green'
        elif total_players > 3 and self.player == players[3]:
            return 'yellow'
        else:
            return None

    def move(self, token):
        color = self.color()
        roll = self.rolls[f'{self.player.id}']
        strtoken = f'{color}-{token}'
        knock = False

        # Check if in base, move to entrance if found
        if strtoken in self.state['bases'][color]:
            knock = self.move_knock(self.state['fields'][ENTRANCES[color]])
            self.state['fields'][ENTRANCES[color]] = strtoken
            self.state['bases'][color][token - 1] = None

        # Move on field
        elif strtoken in self.state['fields']:
            field_index = self.state['fields'].index(strtoken)
            move_to = self.field_wrap(field_index + roll)

            # Move into home or further on the field
            entrance_plus_index = self.entrance_wrap(color, field_index)
            if field_index < entrance_plus_index and move_to >= ENTRANCES[color]:
                move_to = self.field_wrap(move_to - entrance_plus_index)
                self.state['homes'][color][move_to] = strtoken
            else:
                knock = self.move_knock(self.state['fields'][move_to])
                self.state['fields'][move_to] = strtoken

            self.state['fields'][field_index] = None

        # Move further into home
        elif strtoken in self.state['homes'][color]:
            field_index = self.state['homes'][color].index(strtoken)
            move_to = field_index + roll
            self.state['homes'][color][move_to] = strtoken
            self.state['homes'][color][field_index] = None

        return knock

    def move_knock(self, knock_token):
        # Knock enemy token out if one exists on that field
        if knock_token:
            knock_color = self.token_color(knock_token)
            knock_index = self.token_index(knock_token) - 1
            self.state['bases'][knock_color][knock_index] = knock_token
            return True

        return False

    def available_actions(self):
        color = self.color()
        roll = self.rolls[f'{self.player.id}']

        actions = []

        # Spawn tokens on 6 if entrance clear of friendlies
        entrance = self.state['fields'][ENTRANCES[color]]
        if roll == 6 and (not entrance or color not in entrance):
            for strtoken in self.filter(self.state['bases'][color]):
                actions.append(f'move-{self.token_index(strtoken)}')

        # Move any tokens further up the field or into home
        for field_index, strtoken in enumerate(self.state['fields']):
            if strtoken and color == self.token_color(strtoken):
                move_to = self.field_wrap(field_index + roll)
                field_to = self.state['fields'][move_to]

                # Check if in range of home (not at start) or empty or enemy field
                entrance_plus_index = self.entrance_wrap(color, field_index)
                valid = True
                if field_index < entrance_plus_index and move_to >= ENTRANCES[color]:
                    move_to = self.field_wrap(move_to - entrance_plus_index)
                    if move_to > 3:
                        valid = False
                    else:
                        field_to = self.state['homes'][color][move_to]

                if valid and (not field_to or color not in field_to):
                    actions.append(f'move-{self.token_index(strtoken)}')

        # Move tokens in home further into home
        for field_index, strtoken in enumerate(self.state['homes'][color]):
            if strtoken:
                move_to = field_index + roll
                if move_to <= 3:
                    field_to = self.state['homes'][color][move_to]
                    if not field_to:
                        actions.append(f'move-{self.token_index(strtoken)}')

        return actions

    def filter(self, l, color=None):
        return [x for x in l if x]

    def token_color(self, strtoken):
        return strtoken.split('-')[0]

    def token_index(self, strtoken):
        return int(strtoken.split('-')[1])

    def field_wrap(self, field_index):
        return field_index % (39 + 1)

    def entrance_wrap(self, color, field_index):
        # Helper entrance index on red's 39 -> 0 jump
        # 34 is minimum breaking point
        if color == 'red' and field_index > 34:
            return ENTRANCES[color] + 40
        return ENTRANCES[color]


class Room(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ludo_owner')
    users = models.ManyToManyField(User, blank=True, related_name='ludo_users')
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, blank=True, null=True, related_name='ludo_game')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Room [{self.id}, {self.owner}]: {self.name} ({self.users.all()} - {self.game})'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ludo_profile')
    first = models.IntegerField(default=0)
    second = models.IntegerField(default=0)
    third = models.IntegerField(default=0)
    fourth = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.id} Profile (Ludo)'

    def __repr__(self):
        return (
            f'Profile (Ludo) [{self.id}]: played={self.played} (first={self.first},'
            f'second={self.second}, third={self.third}, fourth={self.fourth})'
        )

    def played(self):
        return self.first + self.second + self.third + self.fourth


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Compatibility for Users before Profile addition
    if not hasattr(instance, 'ludo_profile'):
        Profile.objects.create(user=instance)

    instance.ludo_profile.save()
