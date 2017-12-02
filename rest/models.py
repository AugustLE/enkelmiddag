from django.db import models
import os

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from user.models import CustomUser


# Create your models here.

FOOD_TYPES = (
        ('F', 'Fish'),
        ('M', 'Meat'),
        ('C', 'Chicken'),
        ('V', 'Vegetarian'),
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

    #Trengs ikke
    """def delete(self):

        self.image.delete()
        os.remove(self.image.name)
        super(Dinner, self).delete()"""

def ingredient_type_dirctory_path(instance, filename):
    return 'imagedir/ingredientTypes/{0}/{1}'.format(instance.id, filename)

class IngredientType(models.Model):

    name = models.CharField(max_length=100)
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



@receiver(pre_delete, sender=Dinner)
def dinner_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)


@receiver(models.signals.pre_save, sender=Dinner)
def delete_dinner_image_on_change(sender, instance, **kwargs):
    # Deletes old file from filesystem
    # when corresponding `MediaFile` object is updated
    # with new file.

    if not instance.pk:
        return False

    try:
        old_file = Dinner.objects.get(pk=instance.pk).image
    except Dinner.DoesNotExist:
        return False

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

