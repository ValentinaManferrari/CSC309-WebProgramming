from django.db import models
from studios.models import Studio
from accounts.models import OurUser
from django.db.models import CASCADE
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
from django.db.models.lookups import GreaterThan, LessThan
from django.db.models import F
from dateutil.relativedelta import relativedelta
from dirtyfields import DirtyFieldsMixin


# Create your models here.
class Keyword(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)

    def __str__(self):
        return str(self.name)


class Class(DirtyFieldsMixin, models.Model):
    studio = models.ForeignKey(to=Studio, on_delete=CASCADE, related_name='Studio')
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    coach = models.CharField(max_length=200, null=False, blank=False)
    keywords = models.ManyToManyField(to=Keyword, related_name='Keyword', blank=True)
    capacity = models.PositiveIntegerField(null=False, blank=False)

    # Times section
    class_start_date = models.DateField(null=False)
    class_start_time = models.TimeField(null=False)
    class_end_time = models.TimeField(null=False)
    last_class_date = models.DateField(null=False)
    cancelled = models.BooleanField(default=False)

    # Inspiration https://www.geeksforgeeks.org/overriding-the-save-method-django-models
    # https://stackoverflow.com/questions/2307943/django-overriding-the-model-create-method
    def save(self, *args, **kwargs):
        # Check if its the first time a Class obj is created
        create_instances = not self.pk
        changed_fields = self.get_dirty_fields()

        # Must first create the Class object to reference it afterward in Instance object
        super(Class, self).save(*args, **kwargs)

        # If first time, we create the instances
        if create_instances:
            instance_date = self.class_start_date
            final_time = self.last_class_date
            while (instance_date <= final_time):
                Instance.objects.create(
                    class_date=instance_date,
                    class_start=self.class_start_time,
                    class_end=self.class_end_time,
                    cancelled=False,
                    free_spots=self.capacity,
                    class_obj=self,
                )
                instance_date += timedelta(days=7)
        else:

            # NOTE: THIS ASSUMES VALIDATION IS DONE ON ADMIN SIDE!!
            capacity = changed_fields.get('capacity')
            if capacity != None:
                # if diff > 0, we are reducing capacity, otherwise increasing
                diff = capacity - self.capacity
                instances = Instance.objects.filter(class_obj=self).all()
                for ins in instances:
                    ins.free_spots -= diff
                    ins.save()

            if changed_fields.get("time_start") != None or changed_fields.get("time_end") != None:
                time_start = self.class_start_time
                time_end = self.class_end_time
                # if diff > 0, we are reducing capacity, otherwise increasing
                instances = Instance.objects.filter(class_obj=self).all()
                for ins in instances:
                    if time_start != None:
                        ins.class_start = time_start
                    if time_end != None:
                        ins.class_end = time_end
                    ins.save()

            # Last date is changed
            date_end = changed_fields.get("last_class_date")
            if date_end != None:
              # If new date is in the future, try to add new instances
              if date_end < self.last_class_date:
                Instance.objects.filter(class_obj=self)\
                                .filter(GreaterThan(F('class_date'), date_end)) \
                                .update(cancelled=False)
                oldest_instance = Instance.objects.filter(class_obj=self).order_by('class_date').last()
                instance_date = self.class_start_date
                final_time = self.last_class_date
                while (instance_date <= final_time):
                    if instance_date > oldest_instance.class_date:
                      Instance.objects.create(
                          class_date=instance_date,
                          class_start=self.class_start_time,
                          class_end=self.class_end_time,
                          cancelled=False,
                          free_spots=self.capacity,
                          class_obj=self,
                      )
                    instance_date += timedelta(days=7)
              # New date is in the past, 
              elif date_end > self.last_class_date:
                Instance.objects.filter(class_obj=self)\
                                .filter(GreaterThan(F('class_date'), self.last_class_date)) \
                                .update(cancelled = True)

            # First date is changed
            class_start_date = changed_fields.get("class_start_date")
            if class_start_date != None:
              # First of all update all instances to the right week day!
              weekDay_new = self.class_start_date.weekday()
              instances = Instance.objects.filter(class_obj=self).all()
              earliest_date = date(5000, 1, 1)
              for ins in instances:
                ins_week = ins.class_date.isocalendar().week
                ins_year = ins.class_date.isocalendar().year
                ins_date = datetime.strptime(f"{ins_year}-W{ins_week}-{weekDay_new+1}", "%G-W%V-%u").date()
                earliest_date = min(earliest_date, ins_date)
                ins.class_date = ins_date
                if ins_date > self.last_class_date:
                  ins.cancelled = True
                ins.save()

              # Once all instances are updated, add/remove instances if necessary
              # If new date is in the past, try to add new instances
              if class_start_date > self.class_start_date:
                Instance.objects.filter(class_obj=self)\
                                .filter(LessThan(F('class_date'), class_start_date)) \
                                .update(cancelled=False)
                instance_date = self.class_start_date
                final_time = earliest_date
                print(instance_date)
                print(final_time)
                while (instance_date < final_time):
                    print(instance_date)
                    Instance.objects.create(
                        class_date=instance_date,
                        class_start=self.class_start_time,
                        class_end=self.class_end_time,
                        cancelled=False,
                        free_spots=self.capacity,
                        class_obj=self,
                    )
                    instance_date += timedelta(days=7)
              # New date is in the past, 
              elif class_start_date < self.last_class_date:
                Instance.objects.filter(class_obj=self)\
                                .filter(LessThan(F('class_date'), self.class_start_date)) \
                                .update(cancelled = True)
    # https://stackoverflow.com/questions/22947689/django-model-validation-in-admin
    def clean(self):
        cleaned_data = super(Class, self).clean()
        errors = {}
        if not self.class_start_date:
            errors['class_start_date'] = [ValidationError(message='Please input a valid date')]
        if not self.class_start_time:
            errors['class_start_time'] = [ValidationError(message='Please input a valid start time')]
        if not self.class_end_time:
            errors['class_end_time'] = [ValidationError(message='Please input a valid end time')]
        if not self.last_class_date:
            errors['last_class_date'] = [ValidationError(message='Please input a valid last class date')]
        if errors:
            raise ValidationError(errors)

        if self.class_start_time >= self.class_end_time:
            errors['class_end_time'] = [ValidationError(message='Class should end before it starts')]
        if self.class_start_date > self.last_class_date:
            errors['last_class_date'] = [
                ValidationError(message="Can't have last day of class before the first class ends")]
        if errors:
            raise ValidationError(errors)
        return cleaned_data

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "classes"


class Instance(models.Model):
    class_date = models.DateField(null=False)
    class_start = models.TimeField(null=False)
    class_end = models.TimeField(null=False)
    free_spots = models.PositiveIntegerField(null=True, blank=True)
    cancelled = models.BooleanField(default=False)  # Boolean
    class_obj = models.ForeignKey(Class, on_delete=CASCADE, related_name='instances')
    class_start_time = models.DateTimeField(null=False)
    class_end_time = models.DateTimeField(null=False)

    def save(self, *args, **kwargs):
        self.class_start_time = datetime.combine(self.class_date, self.class_start)
        self.class_end_time = datetime.combine(self.class_date, self.class_end)
        super(Instance, self).save(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(Instance, self).clean()
        errors = {}
        if not self.class_date:
            errors['class_date'] = [ValidationError(message='Please input a valid date')]
        if not self.class_start:
            errors['class_start'] = [ValidationError(message='Please input a valid start time')]
        if not self.class_end:
            errors['class_end'] = [ValidationError(message='Please input a valid end time')]
        if errors:
            raise ValidationError(errors)

        if self.class_start >= self.class_end:
            errors['class_end'] = [ValidationError(message='Class should end before it starts')]
        if errors:
            raise ValidationError(errors)
        return cleaned_data


    def __str__(self):
        return f'{self.id} - {self.class_obj} - {self.class_date.strftime("%m/%d/%Y")}'


class Enrollment(models.Model):
    user = models.ForeignKey(OurUser, on_delete=CASCADE, related_name='enrollments')
    class_obj = models.ForeignKey(Class, on_delete=CASCADE, related_name='enrollments')
    instance = models.ForeignKey(Instance, on_delete=CASCADE, related_name='enrollments', null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'class_obj', 'instance'], name='one_enrollment_only'
            )
        ]

##############################################################
########################  Notes  #############################
##############################################################

# Decision: a class represents only one time slot during the week (i.e.
# monday from 16-18), and happens weekly for a fixed period of time
# Why?: For gym lovers, consistency is key, so there is no reason for
# having something like a biweekly class.Also it's easier from a user
# perspective to enroll for a single time slot during the week, than
# having more time slots for a single week and having to manually
# choose the one that suits them for each week.
# Also, we do not allow classes that do not have a last date.

# For now, we also don't allow modifications for class time after
# a class has been created
# Why? From a user's perspective, they pick a time slot that is
# convenient for them. If the coach decides to change the general time of the
# class, it might interfere heavily with a user and then the user would
# require an extra action to cancel all the classes they don't want
# to attend anymore. This might results in classes being filled with
# people that can't attend anymore due to the time change.
# Because of this, we consider it's better for the coaches to not be
# able to change the time of a class.
# For exceptional cases, we allow the coach to reschedule individual
# instances. This will not make user drop the course. a

# Structure for instances:
# Class Extra Fields:
#  - ClassStart       - DateTimeField
#  - ClassEnd         - DateTimeField (Must be after ClassEnd)
#  - LastClassDate    - DateField     (Must be same/after ClassEnd)
#  - Cancelled        - Boolean

# Instances (Automatically generated)
#  - ClassStart       - DateTimeField
#  - ClassEnd         - DateTimeField
#  - Cancelled        - Boolean
#  - class            - ForeignKey

# Note: no middle class for time events because Django doesnt support
# nested inlines, just combine