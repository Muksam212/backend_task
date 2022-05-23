from rest_framework import serializers
from accounts.models import Document, Location, Account, Interest
from django.contrib.auth.models import User


#register serializers
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username','email','password')

    def validate(self, args):
        email = args.get('email', None)
        username = args.get('username', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':{'email already exists'}})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username':{'username already exists'}})

        return super().validate(args)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


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
