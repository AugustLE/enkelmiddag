from django.contrib import admin

from .models import StorePosition, County, City
# Register your models here.
class StoreInLine(admin.StackedInline):

    model = StorePosition
    extra = 0

class CityAdmin(admin.ModelAdmin):

    inlines = [StoreInLine]

class CityInLine(admin.StackedInline):

    model = City
    extra = 0

class CountyAdmin(admin.ModelAdmin):

    inlines = [CityInLine]


admin.site.register(StorePosition)
admin.site.register(City, CityAdmin)
admin.site.register(County, CountyAdmin)