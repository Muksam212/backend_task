from django.urls import path

#Knox provides easy to use authentication for Django REST Framework

from api import views
from api.views import (AccountList, AccountDetails
,DocumentList,DocumentDetails, LocationList, LocationDetails, InterestList, InterestDetails
,DistanceFormula, RandomCoordinate,AccountBulkCreate,AccountBulkUpdate)


#using custom url
app_name = 'api'

urlpatterns = [

    #api for account
    path('api/account/', AccountList.as_view(), name='account-list'),
    path('api/<int:id>/account/', AccountDetails.as_view(), name='account-details'),

    #api for interest
    path('api/interest/', InterestList.as_view(), name='interest-list'),
    path('api/<int:id>/interest/', InterestDetails.as_view(), name='interest-details'),

    #api for document
    path('api/document/', DocumentList.as_view(), name='document-list'),
    path('api/<int:id>/document/', DocumentDetails.as_view(), name='document-details'),

    #api for location
    path('api/location/', LocationList.as_view(), name='location-list'),
    path('api/<int:id>/location/', LocationDetails.as_view(), name='location-details'),


    #to return the geojson
    path('api/<int:id>/account/line/', DistanceFormula.as_view(), name='get-distance'),

    #for the random co-ordinate
    path('api/random/coordinate/',RandomCoordinate.as_view(), name='random-coordinate'),

    #for bulk_create
    path('api/bulkcreate/',AccountBulkCreate.as_view(), name='bulk-create'),
    #for bulk update
    path('api/bulkupdate/', AccountBulkUpdate.as_view(), name='bulk-update'),

    #for api tokens

]
