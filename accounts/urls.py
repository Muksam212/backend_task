from django.urls import path
from .import views
from accounts.views import BirthdayWishUser

app_name='accounts'

urlpatterns = [
	path('api/birthdaywish/', BirthdayWishUser.as_view(), name='birthday-wish')
]