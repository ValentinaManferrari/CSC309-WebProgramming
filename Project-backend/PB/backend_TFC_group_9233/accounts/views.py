from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, CreateAPIView, UpdateAPIView
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from accounts.models import OurUser
from accounts.serializers import UserSerializer
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
import re

# Create your views here.

class SignUp(APIView):
  serializer_class = UserSerializer
  def post(self, request, *args, **kwargs):
    username    = request.POST.get('username')      
    password    = request.POST.get('password')      
    password2   = request.POST.get('password2')      
    email       = request.POST.get('email')  
    first_name  = request.POST.get('first_name')        
    last_name   = request.POST.get('last_name')
    avatar      = request.POST.get('avatar')
    phone       = request.POST.get('phone')

    required_fields = {
      "username_field": username != '',
      "password_field": password != '',
      "password2_field": password2 != ''
    }

    required_OK = required_fields["username_field"] and required_fields["password_field"] and required_fields["password2_field"]

    errors = []
    if password != password2:
      errors += ["The two password fields didn't match"]
    if len(password) < 8:
      errors += ["This password is too short. It must contain at least 8 characters"]
    if OurUser.objects.filter(username=username).exists():
      errors += ["A user with that username already exists"]
    
    # input checking for non-required fields
    phone_regex = re.compile("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
    if 'phone' in request.POST and phone != "":
        if not phone_regex.match(phone):
          errors += ["Phone number is invalid. Please input phone ###-###-####"]

    if not errors and required_OK:
        try:
            user = OurUser.objects.create_user(  # type: ignore
              username  = username  , 
              password  = password  ,
              email     = email     ,
              first_name= first_name,
              last_name = last_name 
              )
        except IntegrityError as e:
          return Response({
            'errors': f"Something went wrong when creating user: {e}",
            'status': 'User not created'
          })
    else:
      return Response({
        'errors': errors,
        'status': 'User not created'
      })
    return Response({
      'username'    : username,   
      'email'       : email,  
      'first_name'  : first_name,  
      'last_name'   : last_name,  
      'avatar'      : avatar,  
      'phone'       : phone,  
    })

class EditProfile(UpdateAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = UserSerializer

  my_bad_response = lambda e : Response({
        'message': f"Something went wrong when updating user",
        'exception': str(e),
        'status': 'User profile not updated'
      }, status=status.HTTP_404_NOT_FOUND)

  # Tried using patch, was getting exception: ".accepted_renderer not set on Response"
  def put(self, request, *args, **kwargs):
    try:
      return super().put(request, *args, **kwargs)
    except ValidationError as e:
      return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)
  
  def patch(self, request, *args, **kwargs):
    try:
      return super().patch(request, *args, **kwargs)
    except ValidationError as e:
      return Response(e.message_dict, status=status.HTTP_400_BAD_REQUEST)

  def get_object(self):
    return get_object_or_404(OurUser, username=self.request.user.username)



# Maybe reuse them to create session based authentication

# class LogIn(APIView):
#   def post(self, request, *args, **kwargs):
#     username = request.POST.get('username','')
#     password = request.POST.get('password','')

#     user = authenticate(request, username=username, password=password)
#     if not user:
#       return Response({
#         'error': "User or password incorrect."
#       })
#     login(request, user)

#     return Response({
#       'username' : username
#     })

# class LogOut(APIView):
#   def post(self, request, *args, **kwargs):
#     logout(request)
#     return Response({
#       'Status': "Logout successful"
#     })
