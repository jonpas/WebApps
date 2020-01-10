from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    name = models.CharField(max_length=20)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ludo_owner')
    users = models.ManyToManyField(User, blank=True, related_name='ludo_users')
    # TODO game = models.ForeignKey(Game, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Room [{self.id}, {self.owner}]: {self.name} ({self.users.all()})'  # TODO - {self.game})'


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
