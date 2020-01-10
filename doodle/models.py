from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import random


class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='player')
    word = models.CharField(max_length=20)
    players_played = models.ManyToManyField(User, blank=True)
    start_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.word} - {self.player}'

    def __repr__(self):
        return f'Game [{self.id}]: {self.word} - {self.player} ({self.players_played.all()})'


class Room(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doodle_owner')
    users = models.ManyToManyField(User, blank=True, related_name='doodle_users')
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Room [{self.id}, {self.owner}]: {self.name} ({self.users.all()} - {self.game})'

    def get_random_user(self):
        max_id = self.users.all().aggregate(max_id=models.Max('id'))['max_id']
        while True:
            pk = random.randint(1, max_id)
            user = self.users.filter(pk=pk).first()
            return user

    def get_random_word(self):
        words = [
            'bee', 'snake', 'cat', 'street', 'cake', 'book', 'car', 'truck', 'dolphin', 'computer',
            'gun', 'keyboard', 'mouse', 'human', 'hair', 'ears', 'nose', 'eyes', 'feet', 'foot',
            'table', 'house', 'door', 'garage', 'light', 'darkness', 'bone', 'food', 'plate', 'fork',
            'spoon', 'knife', 'stick', 'temple', 'sea', 'boat', 'pirate', 'hand', 'notebook', 'pen',
            'glasses', 'backpack', 'laptop', 'phone', 'sleep', 'bed', 'chair', 'spaceship', 'key', 'elephant'
        ]
        return random.choice(words)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doodle_profile')
    played = models.IntegerField(default='0')  # Number of times player was drawing
    wins = models.IntegerField(default='0')
    points = models.IntegerField(default='0')

    def __str__(self):
        return f'{self.user.id} Profile (Doodle)'

    def __repr__(self):
        return f'Profile (Doodle) [{self.id}]: played={self.played}, wins={self.wins}, points={self.points}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Compatibility for Users before Profile addition
    if not hasattr(instance, 'doodle_profile'):
        Profile.objects.create(user=instance)

    instance.doodle_profile.save()
