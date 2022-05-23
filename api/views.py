from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.http import Http404, JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core import exceptions

from math import sin, cos, radians
import uuid

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status,serializers
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import Location, Account, Interest
from accounts.models import Account, Document, Interest, Location

from api.serializers import (AccountSerializer, DocumentSerializer, InterestSerializer, LocationSerializer, RegisterSerializer)


# Create your views here.
#registration api views
class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        # serializer.is_valid(raise_exception = True)
        # serializer.save()
        if(serializer.is_valid()):
            serializer.save()
            return Response({
                'RequestId': str(uuid.uuid4()),
                'Message':'User Created Successfully',
                'User':serializer.data},
            status=status.HTTP_201_CREATED)
        return Response({'Errors':serializers.errors}, status=status.HTTP_400_BAD_REQUEST)

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
    authentication_classes=[JWTAuthentication]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    ordering_fields=['username',]

class AccountDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'



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
        return HttpResponse("Successful")



#calculate the distance by taking random co-ordinate
class RandomCoordinate(APIView):
    def get(self, request):
        account = Account.objects.all()
        return get_object_or_404(account)

    #by taking the random co-ordinate
    def post(self, request):
        self.lat1 = radians(27.7493)
        self.lon1 = radians(85.3214)
        self.lat2 = radians(27.6723547)
        self.lon2 = radians(85.3140242)

        self.dlon=self.lon2-self.lat1
        self.dlat=self.lat2-self.lat1

        self.a=(sin(self.dlat/2)**2+cos(self.lat1)*cos(self.lat2)*sin(self.dlon/2)**2)
        print({"Result of random co-ordinate":self.a})
        return HttpResponse("successful:")


#bulk create using through
class AccountBulkCreate(APIView):
    def post(self, request):
        accounts_obj = [
            {
                'username': 2,
                'country':'Nepal',
                'biography': 'EthicalHacker',
                'phone_number': 9878675645,
                'birthday': '2022-3-2',
                'area_of_interest': 1,
            },
            {
                'username': 3,
                'country':'China',
                'biography': 'Game Development',
                'phone_number': 9878675646,
                'birthday': '2022-3-3',
                'area_of_interest': 2,
            }
        ]

        new = list()
        for a in accounts_obj:
            try:
                u = User.objects.get(id=a['username'])
            except ObjectDoesNotExist:
                pass
            else:
                if not Account.objects.filter(username = u).exists():
                    a['username'] = u
                    new.append(a)

        data = list()
        for n in new:
            data.append(
                Account(
                    username = n['username'],
                    country = n['country'],
                    biography = n['biography'],
                    phone_number= n['phone_number'],
                    birthday = n['birthday']
                    ))
        obj = Account.objects.bulk_create(data)
        temp = list()
        for n in new:
            try:
                acc = Account.objects.get(username=n['username'])
            except ObjectDoesNotExist:
                pass
            else:
                try:
                    interest=Interest.objects.get(id = n['area_of_interest'])
                except ObjectDoesNotExist:
                    pass
                else:
                    temp.append(
                            Account.area_of_interest.through(
                                account = acc,
                                interest = interest
                            )
                        )
                    Account.area_of_interest.through.objects.bulk_create(temp, ignore_conflicts = True)

        data = AccountSerializer(Account.objects.all(), many = True).data
        return Response(data, status = status.HTTP_201_CREATED)

#for bulk update
class AccountBulkUpdate(APIView):
    def post(self, request):
        accounts_obj = [
            {
                'username': 2,
                'country':'China',
                'biography': 'EthicalHacker',
                'phone_number': 100,
                'birthday': '2022-3-2',
                'area_of_interest': [1],
            },
            {
                'username': 3,
                'country':'Japan',
                'biography': 'Data Visualization',
                'phone_number': 10033,
                'birthday': '2022-3-14',
                'area_of_interest': [2],
            }
        ]

        updates = list()
        for a in accounts_obj:
            try:
                acc = Account.objects.prefetch_related('area_of_interest').get(username__id = a['username'])
            except ObjectDoesNotExist:
                pass
            else: 
                acc.area_of_interest.clear()

        #update the data using prefetch_related
        for a in accounts_obj:
            try:
                acc = Account.objects.prefetch_related('area_of_interest').get(username__id = a['username'])
            except ObjectDoesNotExist:
                pass
            else: 
                for i in a['area_of_interest']:
                    try:
                        interest = Interest.objects.get(id = i)
                    except ObjectDoesNotExist:
                        pass
                    else:        
                        acc.area_of_interest.add(interest)

        return Response(status = status.HTTP_201_CREATED)

