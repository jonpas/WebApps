from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Room(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Room [{self.id}]: {self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doodle_profile')
    played = models.IntegerField(default='0')
    wins = models.IntegerField(default='0')
    points = models.IntegerField(default='0')


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
