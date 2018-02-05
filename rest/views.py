from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from user.models import CustomUser
from .serializers import UserSerializer
from rest_framework import status
from PIL import Image

from .models import Dinner, IngredientType, Week
from .serializers import DinnerSerializer, IngredientSerializer, WeekSerializer, IngredientTypeSerializer

class UserList(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserAuth(APIView):

    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"error": "Login failed"}, status=status.HTTP_401_UNAUTHORIZED)

        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class UserAuthToken(ObtainAuthToken):

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            user = serializer.validated_data['user']
            Token.objects.filter(user=user).delete()
            token, created = Token.objects.get_or_create(user=user)

            #if not created:
                # update the created time of the token to keep it valid
             #   token.created = datetime.datetime.utcnow()
              #  token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def image_view(request, dinner_id):

    #if request.user.us_authenticated:
     #   print("True")
    print(request.data)
    dinner = get_object_or_404(Dinner, pk=dinner_id)
    url = "media/" + dinner.image.name
    pdf = open(url, "rb").read()
    return HttpResponse(pdf, content_type='image/png')


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class ImageDinnerView(APIView):

    def get(self, request, dinner_id, format=None):
        print(self.get_renderer_context())
        dinner = get_object_or_404(Dinner, pk=dinner_id)
        url = "media/" + dinner.image.name
        image = open(url, "rb").read()
        return HttpResponse(image, content_type='image/png')


class ImageWeekView(APIView):

    def get(self, request, week_id, format=None):
        print(self.get_renderer_context())
        week = get_object_or_404(Week, pk=week_id)
        url = "media/" + week.image.name
        image = open(url, "rb").read()
        return HttpResponse(image, content_type='image/png')


@api_view(['GET'])
# @permission_classes((permissions.IsAdminUser, ))
def image_view_ing_type(request, ing_type_id):
    print("image_view_ing_type")
    ing_type = get_object_or_404(IngredientType, pk=ing_type_id)
    url = "media/" + ing_type.image.name
    image = open(url, "rb").read()
    return HttpResponse(image, content_type='image/png')


class DinnerList(APIView):
    #permission_classes = (permissions.IsAdminUser,)
    @csrf_exempt
    def get(self, request, format=None):

        dinners = Dinner.objects.filter(visible=True)
        serializer = DinnerSerializer(dinners, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):

        serializer = DinnerSerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class DinnersByCategory(APIView):

    @csrf_exempt
    def get(self, request, dinner_type, format=None):
        dinners = Dinner.objects.filter(type=dinner_type, visible=True)
        print('type type')
        print(dinner_type)
        serializer = DinnerSerializer(dinners, many=True)
        return Response(serializer.data)

class DinnerDetail(APIView):
    #permission_classes = (permissions.IsAdminUser,)
    def get_dinner(self, pk):

        try:
            return Dinner.objects.get(pk=pk, visible=True)
        except Dinner.DoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk, format=None):

        dinner = self.get_dinner(pk)
        serializer = DinnerSerializer(dinner, many=False, context={'request': request})
        if not dinner:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

    def post(self):
        pass

class WeekList(APIView):

    @csrf_exempt
    def get(self, request, format=None):
        weeks = Week.objects.filter(visible=True)
        serializer = WeekSerializer(weeks, many=True)
        return Response(serializer.data)

class WeekDetail(APIView):

    def get_week(self, pk):

        try:
            return Week.objects.get(pk=pk, visible=True)
        except Week.DoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk, format=None):

        week = self.get_week(pk)
        serializer = WeekSerializer(week, many=False, context={'request': request})
        if not week:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data)

class WeekDinners(APIView):

    def get_week(self, pk):

        try:
            return Week.objects.get(pk=pk, visible=True)
        except Week.DoesNotExist:
            return None

    @csrf_exempt
    def get(self, request, pk, format=None):

        week = self.get_week(pk)
        week_dinners = {'name': week.name, 'dinners': {}}

        if week.monday:
            monday = DinnerSerializer(Dinner.objects.get(pk=week.monday.pk), many=False)
            monday_obj = {'monday': monday.data}
            week_dinners['dinners']['monday'] = monday.data
            week_dinners['dinners']['monday_amount'] = week.monday_amount
        if week.tuesday:
            tuesday = DinnerSerializer(Dinner.objects.get(pk=week.tuesday.pk), many=False)
            week_dinners['dinners']['tuesday'] = tuesday.data
            week_dinners['dinners']['tuesday_amount'] = week.tuesday_amount
        if week.wednesday:
            wednesday = DinnerSerializer(Dinner.objects.get(pk=week.wednesday.pk), many=False)
            week_dinners['dinners']['wednesday'] = wednesday.data
            week_dinners['dinners']['wednesday_amount'] = week.wednesday_amount
        if week.thursday:
            thursday = DinnerSerializer(Dinner.objects.get(pk=week.thursday.pk), many=False)
            week_dinners['dinners']['thursday'] = thursday.data
            week_dinners['dinners']['thursday_amount'] = week.thursday_amount
        if week.friday:
            friday = DinnerSerializer(Dinner.objects.get(pk=week.friday.pk), many=False)
            week_dinners['dinners']['friday'] = friday.data
            week_dinners['dinners']['friday_amount'] = week.friday_amount
        if week.saturday:
            saturday = DinnerSerializer(Dinner.objects.get(pk=week.saturday.pk), many=False)
            week_dinners['dinners']['saturday'] = saturday.data
            week_dinners['dinners']['saturday_amount'] = week.saturday_amount
        if week.sunday:
            sunday = DinnerSerializer(Dinner.objects.get(pk=week.sunday.pk), many=False)
            week_dinners['dinners']['sunday'] = sunday.data
            week_dinners['dinners']['sunday_amount'] = week.sunday_amount

        if not week:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(week_dinners)


class IngredientTypeList(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        ingredientTypes = IngredientType.objects.all()
        serializer = IngredientTypeSerializer(ingredientTypes, many=True)
        return Response(serializer.data)