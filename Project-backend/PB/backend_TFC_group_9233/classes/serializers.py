from rest_framework.serializers import ModelSerializer, SlugRelatedField, CharField
from classes.models import Class, Keyword, Instance, Enrollment
from studios.models import Studio, Amenity


class KeywordSerializer(ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['name']


class InstanceSerializerSimple(ModelSerializer):
    class Meta:
        model = Instance
        fields = ['id', 'class_date', 'class_start', 'class_end', 'free_spots', 'cancelled', 'class_obj']


class ClassSerializerSimple(ModelSerializer):
    # https://stackoverflow.com/questions/18012665/how-can-one-customize-django-rest-framework-serializers-output
    keywords = SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'studio', 'name', 'description', 'coach', 'keywords', 'capacity',
                  'class_start_date', 'class_start_time', 'class_end_time', 'last_class_date', 'cancelled']


#####################
# Nested Serializers#
#####################

class InstanceSerializerFull(ModelSerializer):
    class_obj = ClassSerializerSimple(many=False, read_only=True)

    class Meta:
        model = Instance
        fields = ['id', 'class_date', 'class_start', 'class_end', 'free_spots', 'cancelled', 'class_obj']


class ClassSerializerFull(ModelSerializer):
    # https://stackoverflow.com/questions/18012665/how-can-one-customize-django-rest-framework-serializers-output
    keywords = SlugRelatedField(slug_field='name', many=True, read_only=True)
    instances = InstanceSerializerSimple(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'studio', 'name', 'description', 'coach', 'keywords', 'capacity',
                  'class_start_date', 'class_start_time', 'class_end_time', 'last_class_date', 'cancelled'
            , 'instances']


class EnrollSerializerSimple(ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['class_obj', 'instance']


class EnrollSerializerFull(ModelSerializer):
    class_obj = ClassSerializerSimple(many=False, read_only=True)
    instance = InstanceSerializerSimple(many=False, read_only=True)

    class Meta:
        model = Enrollment
        fields = ['user', 'class_obj', 'instance']
