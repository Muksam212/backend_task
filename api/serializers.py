from rest_framework import serializers
from accounts.models import Document, Location, Account, Interest
from django.contrib.auth.models import User

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id','interest_name']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id','file']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id','latitude','longitude']

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','country','bio','ph_number','area_of_interest','users_document','birthday','location_home','location_office']
        depth = 1

    @property
    def schedule_task(self):
        if self.birthday == "2022-05-04":
            return "Happy Birthday Sachin"
        elif self.birthday == "2022-05-01":
            return 'Happy Birthday Muksam'
        else:
            return HttpResponse("None of User have a birthday")

#user authentication
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','email','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        return user
