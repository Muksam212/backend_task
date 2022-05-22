from rest_framework import serializers
from accounts.models import Document, Location, Account, Interest
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields=('username','country','biography','phone_number','birthday','area_of_interest')
        depth = 1

class InterestSerializer(serializers.ModelSerializer):
    #this is called nested serializers
    accounts=AccountSerializer(many=True, read_only=True)
    class Meta:
        model = Interest
        fields = ('id','accounts')

class DocumentSerializer(serializers.ModelSerializer):
    #this is called nested serializer
    accounts=AccountSerializer(many=True, read_only=True)
    class Meta:
        model = Document
        fields = ('id','accounts')


class LocationSerializer(serializers.ModelSerializer):
    #this is called nested serializer
    users_home=AccountSerializer(many=True, read_only=True)
    users_office=AccountSerializer(many=True, read_only=True)
    class Meta:
        model = Location
        fields = ('id','users_home','users_office')


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
