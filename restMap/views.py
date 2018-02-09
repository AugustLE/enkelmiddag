from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from background_task import background

from .RemaCrawler import crawlRema
from .SparCrawler import crawlSpar
from .JokerCrawler import crawlJoker
from .KiwiCrawler import crawlKiwi

from .models import County, City, StorePosition
from .serializers import StoreSerializer, CitySerializer, CountySerializer


def updateWithCities(data, store_brand):

    for county in data['counties']:

        county_name = county['name'].lower().strip()
        county_lat = float(county['lat'])
        county_lng = float(county['lng'])

        try:
            county_object = County.objects.get(name=county_name)
            del_county_stores = StorePosition.objects.filter(county=county_object, store_brand=store_brand)
            for del_store_c in del_county_stores:
                del_store_c.delete()
        except County.DoesNotExist:
            county_object = County(name=county_name, latitude=county_lat, longitude=county_lng)
            county_object.save()
        for city in county['cities']:

            city_name = city['name']
            city_lat = float(city['lat'])
            city_lng = float(city['lng'])

            try:
                city_object = City.objects.get(name=city_name)
                del_stores = StorePosition.objects.filter(city=city_object, store_brand=store_brand)
                for del_store in del_stores:
                    del_store.delete()
            except City.DoesNotExist:
                city_object = City(name=city_name, latitude=city_lat, longitude=city_lng, county=county_object)
                city_object.save()
            for store in city['stores']:
                store_name = store['name']
                store_lat = float(store['lat'])
                store_lng = float(store['lng'])
                phone = store['phone']
                email = store['email']
                address = store['address']
                opening_hours = store['opening_hours']

                phone = phone.replace(' ', '')
                phone = phone.replace('  ', '')
                phone = phone.replace('   ', '')

                store_object = StorePosition(
                    name=store_name,
                    opening_hours=opening_hours,
                    latitude=store_lat,
                    longitude=store_lng,
                    city=city_object,
                    email=email,
                    phone=phone,
                    address=address,
                    county=county_object,
                    store_brand=store_brand
                )
                store_object.save()


def updateWithCounties(data, store_brand):

    for county in data['counties']:

        county_name = county['name'].lower().strip()
        county_lat = float(county['lat'])
        county_lng = float(county['lng'])

        try:
            county_object = County.objects.get(name=county_name)
            del_county_stores = StorePosition.objects.filter(county=county_object, store_brand=store_brand)
            for del_store_c in del_county_stores:
                del_store_c.delete()
        except County.DoesNotExist:
            county_object = County(name=county_name, latitude=county_lat, longitude=county_lng)
            county_object.save()

        for store in county['stores']:
            store_name = store['name']
            store_lat = float(store['lat'])
            store_lng = float(store['lng'])
            phone = store['phone']
            email = store['email']
            address = store['address']
            opening_hours = store['opening_hours']

            phone = phone.replace(' ', '')
            phone = phone.replace('  ', '')
            phone = phone.replace('   ', '')

            store_object = StorePosition(
                name=store_name,
                opening_hours=opening_hours,
                latitude=store_lat,
                longitude=store_lng,
                email=email,
                phone=phone,
                address=address,
                county=county_object,
                store_brand=store_brand
            )
            store_object.save()


@background
def backgroundRema():
    data = crawlRema()
    updateWithCities(data, 'rema')

@background
def backgroundKiwi():
    data = crawlKiwi()
    updateWithCities(data, 'kiwi')

@background
def backgroundJoker():
    data = crawlJoker()
    updateWithCounties(data, 'joker')

@background
def backgroundSpar():
    data = crawlSpar()
    updateWithCounties(data, 'spar')


def updateRema(request):

    backgroundRema()
    return HttpResponse('<h2>Rema is being updated</h2>')


def updateKiwi(request):
    backgroundKiwi()
    return HttpResponse('<h2>Kiwi stores updated</h2>')


def updateJoker(request):
    backgroundJoker()
    return HttpResponse('<h2>Joker stores updated</h2>')


def updateSpar(request):
    backgroundSpar()
    return HttpResponse('<h2>Spar stores updated</h2>')


class GetStores(APIView):
    #permission_classes = (permissions.IsAdminUser,)
    @csrf_exempt
    def get(self, request, format=None):

        stores = StorePosition.objects.all()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)
