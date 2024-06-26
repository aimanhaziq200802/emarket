from django.db import models
from django.contrib.auth.models import AbstractUser

class Location(models.Model):
    name = models.CharField(max_length=35)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('delivery service', 'Delivery service'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    covered_locations = models.ManyToManyField(Location, related_name='sellers', blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
