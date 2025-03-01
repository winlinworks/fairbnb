from django.db import models

from src.db.users.models import User


# Property model
class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  # may want an enum type
    image = models.URLField()
    location = models.CharField(max_length=100)  # may want to address object
    description = models.TextField()
    guests = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    baths = models.IntegerField()
    amenities = models.JSONField(default=list)  # may want enum type
    price = models.FloatField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
