from django.contrib import admin
from studios.models import Studio, Amenity, StudioImage
# Register your models here.


class ImageInline(admin.TabularInline):
    model = StudioImage
    extra = 0
    fields = ['upload']
class AmenityInline(admin.TabularInline):
    model = Amenity
    extra = 0
    fields = ['type', 'quantity']


class StudioAdmin(admin.ModelAdmin):
    fields = ['name', 'address', 'location', 'postal_code', 'phone']
    list_display = ['name', 'address', 'postal_code', 'phone']
    list_display_link = ['name']
    inlines = [ImageInline, AmenityInline]

admin.site.register(Studio, StudioAdmin)
# admin.site.register(Amenity)
# admin.site.register(StudioImage)

