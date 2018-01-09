from django.contrib import admin

from .models import Dinner, Ingredient, IngredientType, StorePosition, Kommune, Fylke, Week

class IngredientInLine(admin.StackedInline):

    model = Ingredient
    extra = 0

class DinnerAdmin(admin.ModelAdmin):

    inlines = [IngredientInLine]
    
class StoreInLine(admin.StackedInline):

    model = StorePosition
    extra = 0

class KommuneAdmin(admin.ModelAdmin):

    inlines = [StoreInLine]


class KommuneInLine(admin.StackedInline):

    model = Kommune
    extra = 0

class FylkeAdmin(admin.ModelAdmin):

    inlines = [KommuneInLine]

admin.site.register(Dinner, DinnerAdmin)
admin.site.register(Ingredient)
admin.site.register(IngredientType)
admin.site.register(StorePosition)
admin.site.register(Kommune, KommuneAdmin)
admin.site.register(Fylke, FylkeAdmin)
admin.site.register(Week)


