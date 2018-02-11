from django.db import models

# Create your models here.
class County(models.Model):

    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)

    def __str__(self):
        return self.name

class City(models.Model):

    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    county = models.ForeignKey(County, related_name='counties')

    def __str__(self):
        return self.name


class StorePosition(models.Model):

    name = models.CharField(max_length=100)
    store_brand = models.CharField(max_length=100)
    opening_hours = models.CharField(max_length=300)
    opening_hours_w = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    city = models.ForeignKey(City, related_name='stores', null=True, blank=True)
    county = models.ForeignKey(County, related_name='county_stores', null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=8, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

