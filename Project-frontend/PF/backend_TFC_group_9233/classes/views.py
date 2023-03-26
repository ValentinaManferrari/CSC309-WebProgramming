from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.db import IntegrityError
from django.db.models.lookups import GreaterThan, LessThan
from django.db.models import F
from django.utils import timezone
from classes.models import Class, Instance, Enrollment
from classes.serializers import InstanceSerializerFull, ClassSerializerFull, EnrollSerializerSimple, EnrollSerializerFull
from studios.models import Studio
from datetime import datetime
from classes.filters import ClassInstanceFilter
from django_filters import rest_framework as filters
from subscriptions.utils import user_subscription

# Get all classes of a studio
class GetAllStudioClasses(ListAPIView):
    serializer_class = ClassSerializerFull

    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        try:
            studio = Studio.objects.get(id=studio_id)
        except Exception as e:
            print(str(e))
            raise NotFound()
        return Class.objects.filter(studio=studio).filter(cancelled=False).all()

    # Gets all instances of classes that are yet to happen


class GetStudioSchedule(ListAPIView):
    serializer_class = InstanceSerializerFull

    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        try:
            studio = Studio.objects.get(id=studio_id)
        except Exception as e:
            print(str(e))
            raise NotFound()
        return Instance.objects \
            .filter(class_obj__studio=studio) \
            .filter(class_obj__cancelled=False) \
            .filter(GreaterThan(F('class_start_time'), datetime.now())) \
            .filter(cancelled=False) \
            .order_by('class_start_time') \
            .all()

    # Helper function that enrolls a user for a specific instance


# Outptu is a code depending on the outcome of the function:
#   0: enrollment successful
#   1: Class is full, can't enroll
#   2: Class is in the past, can't enroll
#   3: Already enrolled in this class
#   4: Other problem
def enroll_instance(user, class_obj, instance):
    print(instance)
    if instance.free_spots == 0:
        return 1
    if instance.class_start_time < timezone.now():
        return 2
    try:
        Enrollment.objects.create(
            user=user,
            class_obj=class_obj,
            instance=instance
        )
    except IntegrityError:
        return 3
    except:
        return 4
    print("here")
    instance.free_spots -= 1
    instance.save()
    return 0


# Enroll in a class or only one instance as a user
class EnrollClass(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollSerializerSimple

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance_id = serializer.data.get('instance')
        class_id = serializer.data.get('class_obj')

        # If user doesn't have a subscription
        if user_subscription(request) == None:
            return Response({"success": False, "message": "You need a subscription to enroll in a course"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            class_obj = Class.objects.get(id=class_id)
            if instance_id != None:
                instance = Instance.objects.get(id=instance_id)
        except:
            return Response({"success": False, "message": "Class or class instance doesn't exist"},
                            status=status.HTTP_404_NOT_FOUND)

        full_past_instances = []
        alr_enrolled_instances = []
        enrolled_instances = []

        # Only dropping one instance
        if instance_id != None:
            enroll_res = enroll_instance(self.request.user, class_obj, instance)
            print(enroll_res)
            if enroll_res == 0:
                enrolled_instances.append(instance)
            elif enroll_res == 1:
                return Response({"success": False, "message": "Class is full"})
            elif enroll_res == 2:
                return Response({"success": False, "message": "Can't enroll in a class from the past"})
            elif enroll_res == 3:
                return Response({"success": False, "message": "Can't enroll in the same class twice", })
        else:
            # If there is no instance provided, user enrolls in the whole class:
            instances = Instance.objects.filter(class_obj=class_obj).all()
            for ins in instances:
                enroll_res = enroll_instance(self.request.user, class_obj, ins)
                # If there are enough spots, enroll
                if enroll_res == 0:
                    enrolled_instances.append(ins)
                elif enroll_res == 1 or enroll_res == 2:
                    full_past_instances.append(ins)
                elif enroll_res == 3:
                    alr_enrolled_instances.append(ins)

        if len(enrolled_instances) == 0:
            return Response({"success": False,
                             "message": "We could not enroll you in any class, because they were all either full or you were already previously enrolled",
                             "full_past_instances": InstanceSerializerFull(full_past_instances, many=True).data,
                             "previously_enrolled_instances": InstanceSerializerFull(alr_enrolled_instances,
                                                                                     many=True).data,
                             }, status=status.HTTP_200_OK)

        return Response({"success": True,
                         "message": "Class enrolled successfully",
                         "enrolled_instances": InstanceSerializerFull(enrolled_instances, many=True).data,
                         "full_past_instances": InstanceSerializerFull(full_past_instances, many=True).data,
                         "previously_enrolled_instances": InstanceSerializerFull(alr_enrolled_instances,
                                                                                 many=True).data,
                         }, status=status.HTTP_201_CREATED)


class DropClass(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollSerializerSimple

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=False)
        instance_id = serializer.data.get('instance')
        class_id = serializer.data.get('class_obj')

        # If user doesn't have a subscription
        if user_subscription(request) == None:
            return Response({"success": False, "message": "You need a subscription to enroll in a course"},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            class_obj = Class.objects.get(id=class_id)
            if instance_id != None:
                instance = Instance.objects.get(id=instance_id)
        except:
            return Response({"success": False, "message": "Class or class instance doesn't exist"},
                            status=status.HTTP_404_NOT_FOUND)

        all_instances = Enrollment.objects.filter(class_obj=class_obj).filter(user=self.request.user)

        # Only dropping one instance
        if instance_id != None:
            enr = all_instances.filter(instance=instance).all()
            if len(enr) == 0:
                return Response({"success": False, "message": "You are not enrolled in this class instance"},
                                status=status.HTTP_404_NOT_FOUND)
            if instance.class_start_time < timezone.now():
                return Response({"success": False, "message": "You can't drop a class in the past"},
                                status=status.HTTP_400_BAD_REQUEST)
            enr.delete()
            instance.free_spots += 1
            instance.save()
        else:
            aux = all_instances.filter(GreaterThan(F('instance__class_start_time'), datetime.now()))
            for enr in aux.all():
                ins = enr.instance
                ins.free_spots += 1
                ins.save()
            all_instances.delete()

        return Response({"success": True, "message": "Class instance(s) dropped successfully"},
                        status=status.HTTP_204_NO_CONTENT)


class UserClassSchedule(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollSerializerFull

    def get_queryset(self):
        user_enrollments = Enrollment.objects \
            .filter(user=self.request.user) \
            .filter(GreaterThan(F('instance__class_start_time'), datetime.now())) \
            .filter(instance__cancelled=False) \
            .order_by('instance__class_start_time') \
            .all()
        return user_enrollments


class UserClassHistory(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EnrollSerializerFull

    def get_queryset(self):
        user_enrollments = Enrollment.objects \
            .filter(user=self.request.user) \
            .filter(LessThan(F('instance__class_start_time'), datetime.now())) \
            .order_by('instance__class_start_time') \
            .all()
        return user_enrollments

# Gets all instances of classes that are yet to happen
class SearchStudioSchedule(ListAPIView):
  serializer_class = InstanceSerializerFull
  filter_backends = (filters.DjangoFilterBackend,)
  filterset_class = ClassInstanceFilter

# Gets all instances of classes that are yet to happen
class SearchStudioSchedule(ListAPIView):
    serializer_class = InstanceSerializerFull
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ClassInstanceFilter

    def get_queryset(self):
        studio_id = self.kwargs.get('studio_id')
        try:
            studio = Studio.objects.get(id=studio_id)
        except Exception as e:
            print(str(e))
            raise NotFound()
        return Instance.objects \
            .filter(class_obj__studio=studio) \
            .filter(class_obj__cancelled=False) \
            .filter(GreaterThan(F('class_start_time'), datetime.now())) \
            .filter(cancelled=False) \
            .order_by('class_start_time') \
            .all()
