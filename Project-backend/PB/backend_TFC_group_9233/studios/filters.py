from django_filters import rest_framework as filters
from studios.models import Studio

class StudioFilter(filters.FilterSet):
  name = filters.CharFilter(field_name="name",  lookup_expr='contains')
  class_name = filters.CharFilter(field_name="Studio__name",  lookup_expr='contains')
  coach = filters.CharFilter(field_name="Studio__coach",  lookup_expr='contains', distinct=True)
  amenity = filters.CharFilter(field_name="amenity__type",  lookup_expr='contains', distinct=True)

  class Meta:
      model = Studio
      unique = True
      fields = [ 'name', 'coach', 'class_name', 'amenity']