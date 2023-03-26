from django.db import models
from django.conf import settings
from location_field.models.plain import PlainLocationField

# Create your models here.

class Studio(models.Model):
    # First name, last name, email, password all included in base model
    # We only need to add extra fields
    name = models.CharField(blank=True, max_length=50)
    address = models.CharField(blank=True, max_length=100)
    
    location = PlainLocationField(based_fields=['city'], default='43.66511259965256,-79.39474806189537')
    latitude = models.FloatField(blank=True,  null=True)
    longitude = models.FloatField(blank=True, null=True)
   
    postal_code = models.CharField(blank=True, max_length=20)
    phone = models.CharField(blank=True, max_length=20)
    
    def save(self, *args, **kwargs):
        coords = self.location.split(',')
        self.latitude = coords[0]
        self.longitude = coords[1]
        super(Studio, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)
    class Meta:
      ordering = ['name']

def image_path(instance, filename):
    return 'media/studio_{0}/{1}'.format(instance.studio_id, filename)
    

class StudioImage(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    upload = models.ImageField(upload_to = image_path)


class Amenity(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    type = models.CharField(blank=True, max_length=20)
    quantity = models.PositiveIntegerField(blank=True)

    class Meta:
        verbose_name_plural = "amenities"
