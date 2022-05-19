from django.shortcuts import render
from django.http import HttpResponse


from rest_framework.views import APIView
from rest_framework import status

from accounts.tasks import send_mail_func

# Create your views here.
class BirthdayWishUser(APIView):
	def post(self,request):
		send_mail_func.delay()
		return Response('Successfull',status = status.HTTP_201_CREATED)
