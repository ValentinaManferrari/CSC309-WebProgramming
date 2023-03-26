from django.urls import path

from accounts.views import SignUp, EditProfile, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView

app_name = 'accounts'

urlpatterns = [
  path('signup/', SignUp.as_view()),
  path('edit_profile/', EditProfile.as_view()),
  path('login/', MyTokenObtainPairView.as_view(), name='login'),
  path('verify_token/', TokenVerifyView.as_view(), name='verify_token'),
]