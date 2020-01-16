from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Transport(models.Model):
    carrier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_carrier')
    passengers = models.ManyToManyField(User, blank=True, related_name='transport_passenger')

    def __str__(self):
        return self.carrier.get_username()

    def __repr__(self):
        return f'Transport [{self.id}]: {self.carrier} ({self.passengers.all()})'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='transport_profile')
    carrier = models.BooleanField(default=False)
    passenger = models.BooleanField(default=False)
    rating1 = models.IntegerField(default=0)
    rating2 = models.IntegerField(default=0)
    rating3 = models.IntegerField(default=0)
    rating4 = models.IntegerField(default=0)
    rating5 = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.id} Profile (Transport): {self.rating_avg()}'

    def __repr__(self):
        return (
            f'Profile (Transport) [{self.id}]: carrier={self.carrier}, passenger={self.passenger} ({self.rating_avg()}:'
            f' 1: {self.rating1}, 2: {self.rating2}, 3: {self.rating3}, 4: {self.rating4}, 5: {self.rating5})'
        )

    def rating_avg(self):
        total = self.rating1 * 1 + self.rating2 * 2 + self.rating3 * 3 + self.rating4 * 4 + self.rating5 * 5
        amount = self.rating1 + self.rating2 + self.rating3 + self.rating4 + self.rating5

        if amount <= 0:
            return 0
        return round(total / amount, 1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Compatibility for Users before Profile addition
    if not hasattr(instance, 'transport_profile'):
        Profile.objects.create(user=instance)

    instance.transport_profile.save()
