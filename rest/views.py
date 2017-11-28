from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import generics
from user.models import CustomUser
from .serializers import UserSerializer
from rest_framework import status

from .models import Dinner, IngredientType

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


def image_view(request, dinner_id):

    dinner = get_object_or_404(Dinner, pk=dinner_id)
    url = "media/" + dinner.image.name
    pdf = open(url, "rb").read()
    return HttpResponse(pdf, content_type='application/png')

def image_view_ing_type(request, ing_type_id):

    ing_type = get_object_or_404(IngredientType, pk=ing_type_id)
    url = "media/" + ing_type.image.name
    pdf = open(url, "rb").read()
    return HttpResponse(pdf, content_type='application/png')