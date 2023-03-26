from rest_framework import serializers
from studios.models import Studio, Amenity

class AmenitySerializer(serializers.ModelSerializer):
  class Meta:
    model = Amenity
    fields = ['type']

class StudioSerializer(serializers.ModelSerializer):
  amenity_set = AmenitySerializer(many=True, read_only=True)

  class Meta:
    model = Studio
    fields = ['name', 'address', 'location', 'postal_code', 'phone', 'amenity_set']