from django.urls import path

from studios.views import List_By_Location, Get_Studio_Page, Search_Studios

app_name = 'studios'

urlpatterns = [
  path('list_by_location/', List_By_Location.as_view()),
  path('get_studio_page/<int:studio_id>/', Get_Studio_Page.as_view()),
  path('search_studios/', Search_Studios.as_view()),
]