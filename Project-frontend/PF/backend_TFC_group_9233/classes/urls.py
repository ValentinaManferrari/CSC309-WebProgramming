from django.urls import path

from classes.views import GetStudioSchedule, GetAllStudioClasses, EnrollClass, UserClassHistory, UserClassSchedule, DropClass, SearchStudioSchedule

app_name = 'classes'

urlpatterns = [
  path('get_studio_schedule/<int:studio_id>/', GetStudioSchedule.as_view()),
  path('get_all_studio_classes/<int:studio_id>/', GetAllStudioClasses.as_view()),
  path('enroll_class/', EnrollClass.as_view()),
  path('drop_class/', DropClass.as_view()),
  path('user_class_history/', UserClassHistory.as_view()),
  path('user_class_schedule/', UserClassSchedule.as_view()),
  path('search_studio_schedule/<int:studio_id>/', SearchStudioSchedule.as_view()),
]