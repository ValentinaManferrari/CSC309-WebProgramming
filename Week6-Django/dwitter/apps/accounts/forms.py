from django import forms
# ADDITION: import Django's UserCreationForm
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

# ADDITION: extend the UserCreationForm to add a first_name and last_name and email fields
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=75)