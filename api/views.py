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


#Register through api
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

#Login through API
class LoginAPI(LoginView):
    permission_classes =(permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginAPI,self).post(request,format=None)

#calculate the distance between two points
class DistanceFormula(APIView):
    def get(self, **kwargs):
        id = self.kwargs.get('id')
        return get_object_or_404(Account, id=id)

    def post(self, request, id):
        self.lat1=radians(27.7294)
        self.lon1=radians(85.3502)
        self.lat2=radians(27.6723547)
        self.lon2=radians(85.3140242)

        self.dlon=self.lon2-self.lat1
        self.dlat=self.lat2-self.lat1

        self.a=(sin(self.dlat/2)**2+cos(self.lat1)*cos(self.lat2)*sin(self.dlon/2)**2)
        print({'Result of userline vector using distance formula form home to office':self.a})
        return HttpResponse("successful")


#calculate the distance by taking random co-ordinate
class RandomCoordinate(APIView):
    def get(self, request):
        account = Account.objects.all()
        return get_object_or_404(account)

    #by taking the random co-ordinate
    def post(self, request):
        user=self.request.user
        self.lat1 = radians(27.7493)
        self.lon1 = radians(85.3214)
        self.lat2 = radians(27.6723547)
        self.lon2 = radians(85.3140242)

        self.dlon=self.lon2-self.lat1
        self.dlat=self.lat2-self.lat1

        self.a=(sin(self.dlat/2)**2+cos(self.lat1)*cos(self.lat2)*sin(self.dlon/2)**2)
        print({"Result of random co-ordinate":self.a})
        return HttpResponse("successful:")
