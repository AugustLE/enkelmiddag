from django.contrib import admin

from .models import Dinner, Ingredient, IngredientType, Week
class IngredientInLine(admin.StackedInline):

    model = Ingredient
    extra = 0

class DinnerAdmin(admin.ModelAdmin):

    inlines = [IngredientInLine]

admin.site.register(Dinner, DinnerAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
admin.site.register(Week)


