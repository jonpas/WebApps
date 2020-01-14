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
        if total_players > 1 and self.player == players[1]:
            return 'red'
        if total_players > 2 and self.player == players[2]:
            return 'green'
        if total_players > 3 and self.player == players[3]:
            return 'yellow'

    def move(self, token):
        color = self.color()
        strtoken = f'{color}-{token}'

        # Apply move to state
        # Check in base, move to entrance if found
        if strtoken in self.state['bases'][color]:
            self.state['fields'][ENTRANCES[color]] = strtoken
            self.state['bases'][color][token - 1] = None

        # TODO Move on field

        # TODO Move into home

        # TODO Knock another token
        knock = False

        return knock

    def available_actions(self):
        color = self.color()
        roll = self.rolls[f'{self.player.id}']

        actions = []

        # Spawn tokens on 6 if entrance clear
        if roll == 6 and not self.state['fields'][ENTRANCES[color]]:
            for strtoken in self.filter(self.state['bases'][color]):
                token = self.token_index(strtoken)
                actions.append(f'move-{token}')

        # TODO Move any tokens further up the field
        # TODO Move any tokens into home or further in home

        print(f'available_actions: {actions}')
        return actions

    def filter(self, l):
        return [x for x in l if x]

    def token_index(self, strtoken):
        return strtoken.split('-')[1]


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
    wins = models.IntegerField(default='0')
    seconds = models.IntegerField(default='0')
    thirds = models.IntegerField(default='0')
    fourths = models.IntegerField(default='0')

    def __str__(self):
        return f'{self.user.id} Profile (Ludo)'

    def __repr__(self):
        return f'Profile (Ludo) [{self.id}]: played={self.played}, wins={self.wins}, points={self.points}'

    def played(self):
        return self.wins + self.seconds + self.thirds + self.fourths


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
