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
from .serializers import DinnerSerializer, IngredientSerializer, WeekSerializer

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
    permission_classes = (permissions.IsAdminUser,)
    @csrf_exempt
    def get(self, request, format=None):

        dinners = Dinner.objects.all()
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


class DinnerDetail(APIView):
    permission_classes = (permissions.IsAdminUser,)
    def get_dinner(self, pk):

        try:
            return Dinner.objects.get(pk=pk)
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
        weeks = Week.objects.all()
        serializer = WeekSerializer(weeks, many=True)
        return Response(serializer.data)

