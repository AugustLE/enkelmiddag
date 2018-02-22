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
from .serializers import StoreSerializer, CitySerializer, CountySerializer, SimpleStoreSerializer, PureCitySerializer


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
    return HttpResponse('<h2>Rema is queued for update</h2>')


def updateKiwi(request):
    backgroundKiwi()
    return HttpResponse('<h2>Kiwi is queued for update</h2>')


def updateJoker(request):
    backgroundJoker()
    return HttpResponse('<h2>Joker is queued for update</h2>')


def updateSpar(request):
    backgroundSpar()
    return HttpResponse('<h2>Spar is queued for update</h2>')


class StoreList(APIView):
    #permission_classes = (permissions.IsAdminUser,)
    @csrf_exempt
    def get(self, request, format=None):
        stores = StorePosition.objects.all()
        serializer = SimpleStoreSerializer(stores, many=True)
        return Response(serializer.data)

class CountyList(APIView):

    @csrf_exempt
    def get(self, request, format=None):

        counties = County.objects.all().order_by('name')
        serializer = CountySerializer(counties, many=True)
        return Response(serializer.data)


def packCities(serializerType):
    response = []
    counties = County.objects.order_by('name')

    for county in counties:
        city_data = serializerType(City.objects.filter(county=county), many=True)
        county_object = {"name": county.name, "pk": county.pk, county.name: city_data.data}
        response.append(county_object)

    return response

class CountyCityList(APIView):

    @csrf_exempt
    def get(self, request, format=None):
        response = packCities(CitySerializer)
        return Response(response)

class PureCountyCityList(APIView):

    @csrf_exempt
    def get(self, request, format=None):
        response = packCities(PureCitySerializer)
        return Response(response)


class CountyStoreList(APIView):

    @csrf_exempt
    def get(self, request, pk, format=None):
        county = County.objects.get(pk=pk)
        stores = StorePosition.objects.filter(county=county)
        serializer = SimpleStoreSerializer(stores, many=True)
        return Response(serializer.data)

