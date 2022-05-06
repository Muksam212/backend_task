from django.urls import path
from api import views
from knox import views as knox_views
#Knox provides easy to use authentication for Django REST Framework

from api.views import (AccountList, AccountDetails
,DocumentList,DocumentDetails, LocationList, LocationDetails, InterestList, InterestDetails, LoginAPI,
RegisterAPI,DistanceFormula, RandomCoordinate)


app_name = 'api'

urlpatterns = [
    path('api/account/', AccountList.as_view(), name='account-list'),
    path('api/<int:id>/account/', AccountDetails.as_view(), name='account-details'),

    path('api/interest/', InterestList.as_view(), name='interest-list'),
    path('api/<int:id>/interest/', InterestDetails.as_view(), name='interest-details'),

    path('api/document/', DocumentList.as_view(), name='document-list'),
    path('api/<int:id>/document/', DocumentDetails.as_view(), name='document-details'),

    path('api/location/', LocationList.as_view(), name='location-list'),
    path('api/<int:id>/location/', LocationDetails.as_view(), name='location-details'),

    #register
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView, name='logoutall'),

    #to return the geojson
    path('api/<int:id>/account/line/', DistanceFormula.as_view(), name='get-distance'),


    path('api/random/coordinate/',RandomCoordinate.as_view(), name='random-coordinate')
]
