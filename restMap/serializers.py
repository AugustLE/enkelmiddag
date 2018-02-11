from rest_framework import serializers
from .models import County, City, StorePosition


class StoreSerializer(serializers.ModelSerializer):

    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city.pk')

    class Meta:

        model = StorePosition
        fields = (
            'pk',
            'city_id',
            'opening_hours',
            'opening_hours_w',
            'latitude',
            'longitude',
            'email',
            'phone',
            'address')


class CitySerializer(serializers.ModelSerializer):

    stores = StoreSerializer(many=True)

    class Meta:

        model = City
        fields = ('pk', 'name', 'latitude', 'longitude', 'stores')


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = ('pk', 'name', 'latitude', 'longitude')