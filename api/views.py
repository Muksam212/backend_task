from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.gis.measure import Distance

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


class LocationDistance(APIView):
    def post(self, request):
        serializer = LocationSerializer(data = request.data)

        if serializer.is_valid():
            try:
                print(serializer.data)
                data = serializer.data
                print(data)

                pnt = Distance('Point({} {}'.format(data['latitude'],data['longitude']))
                print(pnt)
                
                ls = Location.objects.all().filter(point__distance__lt=(pnt, Distance(km=1000)))
                print(len(ls))
                return Response({'Data', str(ls)})

            except Exception as e:
                print(e)

        return Response(serializer.errors)