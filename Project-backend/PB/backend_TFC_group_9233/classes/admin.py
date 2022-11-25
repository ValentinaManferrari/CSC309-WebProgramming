from django.contrib import admin
from classes.models import Keyword, Class, Instance, Enrollment
from django.forms import ModelForm, ValidationError


class InstanceInline(admin.TabularInline):
    model = Instance
    fields = ['id', 'class_date', 'class_start', 'class_end', 'free_spots', 'cancelled']
    readonly_fields = ['id', 'free_spots']
    list_display = ['id', 'class_date', 'class_start', 'class_end', 'free_spots', 'cancelled']
    max_num = 0  # Disable add button
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


class ClassAdminForm(ModelForm):
    class Meta:
        model = Class
        fields = '__all__'

    def clean_capacity(self):
        old_capacity = self.instance.capacity
        new_capacity = self.cleaned_data['capacity']
        if old_capacity == None:
            return new_capacity

        # if diff > 0, we are reducing capacity, otherwise increasing
        diff = old_capacity - new_capacity
        bad_instances = Instance.objects.filter(class_obj=self.instance).filter(free_spots__lt=diff).all()
        if len(bad_instances) > 0:
            raise ValidationError(message="Some class instances don't have enough free spots to reduce capacity")
        return new_capacity


# Inspiration from: https://stackoverflow.com/questions/66776107/how-to-show-many-to-many-field-on-django-admin-panel
class ClassAdmin(admin.ModelAdmin):
    fields = ['studio', 'name', 'description', 'coach', 'capacity', 'keywords',
              'class_start_date', 'class_start_time', 'class_end_time', 'last_class_date', 'cancelled']
    list_display = ['id', 'name', 'studio_name', 'coach', 'cancelled']
    list_display_links = ['name']
    filter_horizontal = ('keywords',)
    inlines = [InstanceInline]
    form = ClassAdminForm

    # https://stackoverflow.com/questions/17613559/django-readonly-field-only-on-change-but-not-when-creating
    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return ['class_start_date', 'last_class_date']  # 'class_start_time', 'class_end_time',
        else:
            return []

    def studio_name(self, instance):
        return instance.studio.name


class KeywordAdmin(admin.ModelAdmin):
    list_display = ['name']


# Register your models here.
admin.site.register(Class, ClassAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Instance)  # Should be commented once finished
admin.site.register(Enrollment)  # Should be commented once finished
