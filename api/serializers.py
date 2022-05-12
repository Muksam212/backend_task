from rest_framework import serializers
from accounts.models import Document, Location, Account, Interest
from django.contrib.auth.models import User


class AccountSerializer(serializers.ModelSerializer):
    #nested serializer
    class Meta:
        model=Account
        fields=('username','country','biography','phone_number','birthday')
        depth = 1

class InterestSerializer(serializers.ModelSerializer):
    accounts=AccountSerializer(many=True, read_only=True)
    class Meta:
        model = Interest
        fields = ('id','accounts')

class DocumentSerializer(serializers.ModelSerializer):
    accounts=AccountSerializer(many=True, read_only=True)
    class Meta:
        model = Document
        fields = ('id','accounts')


class LocationSerializer(serializers.ModelSerializer):
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
