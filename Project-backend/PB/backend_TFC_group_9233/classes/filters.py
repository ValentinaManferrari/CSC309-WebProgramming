from django_filters import rest_framework as filters
from classes.models import Instance

class ClassInstanceFilter(filters.FilterSet):
  name = filters.CharFilter(field_name="class_obj__name",  lookup_expr='contains')
  coach = filters.CharFilter(field_name="class_obj__coach",  lookup_expr='contains')
  date = filters.DateFromToRangeFilter(field_name="class_date")
  time_start = filters.TimeFilter(field_name="class_start",  lookup_expr='gte')
  time_end = filters.TimeFilter(field_name="class_end",  lookup_expr='lte')

  class Meta:
      model = Instance
      fields = [ 'name', 'coach', 'date', 'time_start', 'time_end']
