from django.db import models
from accounts.models import Profile
# Create your models here.

class City(models.Model):
    city = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.city}"


class Property(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='property_set')
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    beds = models.IntegerField()
    baths = models.IntegerField()
    sq_feet = models.FloatField()
    info = models.TextField()
    image = models.FileField(upload_to='images/')
    google_map_link = models.CharField(max_length=1000)
    is_new = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}({self.location})"



class Gallery(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="gallery_set")
    image = models.FileField(upload_to=f'images/gallery/')

    def __str__(self):
        return f"{self.property}({self.image.url})"


class Services(models.Model):
    image = models.FileField(upload_to='services/images')
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

class Testmonials(models.Model):
    image = models.FileField(upload_to='testmonials/images')
    name = models.CharField(max_length=100)
    caption = models.TextField()

    def __str__(self):
        return f"{self.name}"

class CarasoulData(models.Model):
    image = models.FileField(upload_to='carasoul/images')
    title = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return f"{self.title}"
