from django.contrib import admin

from .models import Dinner, Ingredient, IngredientType

class IngredientInLine(admin.StackedInline):

    model = Ingredient
    extra = 0

class DinnerAdmin(admin.ModelAdmin):

    inlines = [IngredientInLine]
    def media(self):
        print("Yes okeu")
        return super(DinnerAdmin, self).media


admin.site.register(Dinner, DinnerAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
