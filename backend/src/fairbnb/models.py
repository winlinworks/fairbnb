# Django models for Profiles and Properties

from django.contrib.auth.models import User
from django.db import models


# Profile model
class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )  # User fields include: first_name, last_name, email, password, is_staff, is_active, date_joined, last_login
    image = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)


# Property model
class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # may want an enum type
    image = models.URLField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    amenities = models.JSONField(default=list)
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
