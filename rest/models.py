from django.db import models
import os

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from user.models import CustomUser
from PIL import Image

# Create your models here.

FOOD_TYPES = (
        ('F', 'Fish'),
        ('M', 'Meat'),
        ('C', 'Chicken'),
        ('V', 'Vegetarian'),
    )

INGREDIENT_TYPES = (
    ('O', 'Other'),
    ('F', 'Fruit and Vegetables'),
    ('M', 'Meat and Fish'),
    ('D', 'Milk Products & Egg'),
    ('H', 'Canned Food'),
    ('S', 'Spices'),
    ('Ss', 'Sauces'),
    ('B', 'Baking')
)

def dinner_dirctory_path(instance, filename):
    return 'imagedir/dinners/{0}/{1}'.format(instance.id, filename)

class Dinner(models.Model):

    name = models.CharField(max_length=150)
    type = models.CharField(max_length=100, choices=FOOD_TYPES)
    recipe = models.TextField(max_length=1000)
    owner = models.ForeignKey(CustomUser, related_name='dinners', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=dinner_dirctory_path, null=True, blank=True)
    visible = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.pk is None:

            saved_image = self.image
            self.image = None
            super(Dinner, self).save(*args, **kwargs)
            self.image = saved_image
        super(Dinner, self).save(*args, **kwargs)

def ingredient_type_dirctory_path(instance, filename):
    return 'imagedir/ingredientTypes/{0}/{1}'.format(instance.id, filename)

class IngredientType(models.Model):

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100, choices=INGREDIENT_TYPES, default=INGREDIENT_TYPES[0])
    plural_name = models.CharField(max_length=100, null=True, blank=True)
    singular_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=ingredient_type_dirctory_path, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.image
            self.image = None
            super(IngredientType, self).save(*args, **kwargs)
            self.image = saved_image
        super(IngredientType, self).save(*args, **kwargs)


    def __str__(self):

        return self.name

class Ingredient(models.Model):

    #name = models.CharField(max_length=100)
    type = models.ForeignKey(IngredientType, related_name='ingredients')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    annotation = models.CharField(max_length=20)
    dinner = models.ForeignKey(Dinner, null=True, related_name='ingredients')

    def __str__(self):
        return self.type.name


class Week(models.Model):

    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    monday = models.ForeignKey(Dinner, null=True, blank=True, related_name='monday')
    monday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    tuesday = models.ForeignKey(Dinner, null=True, blank=True, related_name='tuesday')
    tuesday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    wednesday = models.ForeignKey(Dinner, null=True, blank=True, related_name='wednesday')
    wednesday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    thursday = models.ForeignKey(Dinner, null=True, blank=True, related_name='thursday')
    thursday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    friday = models.ForeignKey(Dinner, null=True, blank=True, related_name='friday')
    friday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    saturday = models.ForeignKey(Dinner, null=True, blank=True, related_name='saturday')
    saturday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)
    sunday = models.ForeignKey(Dinner, null=True, blank=True, related_name='sunday')
    sunday_amount = models.DecimalField(decimal_places=1, max_digits=10, null=True, blank=True)

    def __str__(self):
        return self.name



class Fylke(models.Model):

    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)

    def __str__(self):
        return self.name

class Kommune(models.Model):

    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    fylke = models.ForeignKey(Fylke, related_name='kommuner')

    def __str__(self):
        return self.name


class StorePosition(models.Model):

    name = models.CharField(max_length=100)
    opening_hours = models.CharField(max_length=300)
    opening_hours_w = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=20, decimal_places=6)
    longitude = models.DecimalField(max_digits=20, decimal_places=6)
    kommune = models.ForeignKey(Kommune, related_name='storePositions')

    def __str__(self):
        return self.name

@receiver(pre_delete, sender=Dinner)
def dinner_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)


@receiver(models.signals.pre_save, sender=Dinner)
def delete_dinner_image_on_change(sender, instance, **kwargs):
    # Deletes old file from filesystem
    # when corresponding `MediaFile` object is updated
    # with new file.
   #print(sender.request)
    if not instance.pk:
        return False

    try:
        old_file = Dinner.objects.get(pk=instance.pk).image
    except Dinner.DoesNotExist:
        return False

    if (instance.image and instance.image != old_file) or not instance.image:

        old_file.delete(False)


@receiver(pre_delete, sender=IngredientType)
def ingredient_type_delete(sender, instance, **kwargs):

    instance.image.delete(False)

@receiver(models.signals.pre_save, sender=IngredientType)
def delete_ing_type_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False
    try:
        old_file = IngredientType.objects.get(pk=instance.pk).image
    except Dinner.DoesNotExist:
        return False

    old_file.delete(False)

