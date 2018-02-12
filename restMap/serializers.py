from rest_framework import serializers
from .models import County, City, StorePosition


class SimpleStoreSerializer(serializers.ModelSerializer):

    class Meta:

        model = StorePosition
        fields = (
            'pk',
            'name',
            'opening_hours',
            'opening_hours_w',
            'latitude',
            'longitude',
            'email',
            'phone',
            'address')


class StoreSerializer(serializers.ModelSerializer):

    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source='city.pk')

    class Meta:

        model = StorePosition
        fields = (
            'pk',
            'city_id',
            'name',
            'opening_hours',
            'opening_hours_w',
            'latitude',
            'longitude',
            'email',
            'phone',
            'address')


class PureCitySerializer(serializers.ModelSerializer):

    class Meta:

        model = City
        fields = ('pk', 'name', 'latitude', 'longitude')


class CitySerializer(serializers.ModelSerializer):

    stores = StoreSerializer(many=True)

    class Meta:

        model = City
        fields = ('pk', 'name', 'latitude', 'longitude', 'stores')


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = ('pk', 'name', 'latitude', 'longitude')