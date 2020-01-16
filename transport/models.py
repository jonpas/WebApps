from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from multiselectfield import MultiSelectField


class Transport(models.Model):
    class Location(models.TextChoices):
        MARIBOR = 'MB'
        LJUBLJANA = 'LJ'
        KOPER = 'KP'
        CELJE = 'CE'
        MURSKA_SOBOTA = 'MS'

    class VehicleType(models.TextChoices):
        CAR = 'C'
        VAN = 'V'
        TRUCK = 'T'
        LIMOUSINE = 'L'

    class VehicleBrand(models.TextChoices):
        MITSUBISHI = 'MITS'
        AUDI = 'AUDI'
        BMW = 'BMW'
        CITROEN = 'CITR'

    carrier = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_carrier')
    passengers = models.ManyToManyField(User, blank=True, related_name='transport_passenger')
    passengers_confirmed = models.ManyToManyField(User, blank=True,
                                                  related_name='transport_passenger_confirmed')
    departure_time = models.DateTimeField()
    departure_location = models.CharField(max_length=2, choices=Location.choices, default=Location.MARIBOR)
    arrival_location = models.CharField(max_length=2, choices=Location.choices, default=Location.LJUBLJANA)
    price = models.IntegerField(default=100)
    max_passengers = models.IntegerField(default=1)
    luggage_per_passenger = models.IntegerField(default=1)
    vehicle_type = models.CharField(max_length=1, choices=VehicleType.choices, blank=True)
    vehicle_brand = models.CharField(max_length=4, choices=VehicleBrand.choices, blank=True)
    vehicle_color = models.CharField(max_length=100, blank=True)
    vehicle_registration = models.CharField(max_length=10, blank=True)
    passing_locations = MultiSelectField(max_length=2, choices=Location.choices)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.departure_location} > {self.arrival_location} ({self.carrier.get_username()})'

    def __repr__(self):
        return f'Transport [{self.id}]: {self.carrier} ({self.passengers.all()})'

    def free_seats(self):
        return self.max_passengers - self.passengers_confirmed.count()

    def stops_display(self):
        return [self.Location(stop).label
                for stop in self.passing_locations]


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
