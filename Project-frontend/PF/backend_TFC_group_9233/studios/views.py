from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from studios.models import Studio
from studios.serializers import StudioSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from studios.filters import StudioFilter

from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F

# Helper Function for input checking
def isfloat(num):
    try:
        float(num)
        return True
    except:
        return False

# As a user, I want to list studios based on geographical proximity to a specific
# location (e.g., my current location, a pinpoint on map, or a postal code). 
# Studios must list starting from the closest one, each having a drop pin on the map.
class List_By_Location(ListAPIView):
  serializer_class = StudioSerializer
  
  def get_queryset(self):
    lat = self.request.data.get('latitude')
    lon = self.request.data.get('longitude')
    
    #  check if parameter is not passed
    if lat is None:
      raise ValidationError({"success":False, "message": "No Latitude param"})
    if lon is None:
      raise ValidationError({"success":False, "message": "No Longitude param"})
    
    # check if parameter value is correct
    if not isfloat(lat):
      raise ValidationError({"success":False, "message": "Invalid Latitude"}) 
    if not isfloat(lon):
      raise ValidationError({"success":False, "message": "Invalid Longitude"}) 

    latitude  = float(lat)
    longitude = float(lon)
    
    # Reference to:
    # https://stackoverflow.com/questions/17682201/how-to-filter-a-django-model-with-latitude-and-longitude-coordinates-that-fall-w
    dlat = Radians(F('latitude') - latitude)
    dlong = Radians(F('longitude') - longitude )
    a = (Power(Sin(dlat/2), 2) + Cos(Radians(latitude)) 
        * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2))
    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    d = 6371 * c

    # Filter by radius distance only if input is correct, othervise return full list
    if isfloat(self.request.GET.get('radius')):
      radius = float(self.request.GET.get('radius'))
      return Studio.objects.annotate(distance=d).filter(distance__lt=radius).order_by('distance').all()
    
    return Studio.objects.annotate(distance=d).order_by('distance').all()


# As a user, I can click on each of the studios and move to the studio page. 
# This page should contain the general information of that studio, along with 
# its address, location, and a link to get the directions.
class Get_Studio_Page(RetrieveAPIView):
  serializer_class = StudioSerializer
  
  def get_object(self):
      return get_object_or_404(Studio, id=self.kwargs['studio_id'])


# As a user, I want to search/filter through the listed studios (mentioned earlier). 
# Search/filter includes stdio name, amenities, class names, and coaches that hold 
# classes in those studios.
class Search_Studios(ListAPIView):
  serializer_class = StudioSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = StudioFilter
  queryset = Studio.objects.all()

