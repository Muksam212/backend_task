from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.http import Http404, HttpResponse


from math import sin, cos, radians
from accounts.models import Location, Account
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from api.serializers import AccountSerializer, DocumentSerializer, InterestSerializer, LocationSerializer
from rest_framework import generics, mixins
from accounts.models import Account, Document, Interest, Location
from knox.models import AuthToken
from api.serializers import RegisterSerializer, UserSerializer
from knox.views import LoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer



# Create your views here.


#Interest Api
class InterestList(generics.ListCreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class InterestDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    lookup_field = 'id'


#Document Api
class DocumentList(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'id'

#Location Api
class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    lookup_field = 'id'

#Accounts api
class AccountList(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

class LoginAPI(LoginView):
    permission_classes =(permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginAPI,self).post(request,format=None)

class DistanceFormula(APIView):
    def get_object(self, **kwargs):
        id=self.kwargs.get('id')
        return get_object_or_404(Account, id=id)

    def post(self, request, *args, **kwargs):
        self.lat1=radians(45.56)
        self.lon1=radians(34.56)
        self.lat2=radians(33.45)
        self.lon2=radians(45.67)

        self.dlon=self.lon2-self.lat1
        self.dlat=self.lat2-self.lat1

        self.a=(sin(self.dlat/2)**2+cos(self.lat1)*cos(self.lat2)*sin(self.dlon/2)**2)
        print({'Result of userline vector using distance formula form home to office':self.a})
        return HttpResponse("successful")


class RandomCoordinate(APIView):

    #by taking the random co-ordinate
    def post(self, request):
        self.lat1 = radians(22.67)
        self.lon1 = radians(33.78)
        self.lat2 = radians(44.67)
        self.lon2 = radians(55.89)

        self.dlon=self.lon2-self.lat1
        self.dlat=self.lat2-self.lat1

        self.a=(sin(self.dlat/2)**2+cos(self.lat1)*cos(self.lat2)*sin(self.dlon/2)**2)
        print({"Result":self.a})
        return HttpResponse("successful:")
