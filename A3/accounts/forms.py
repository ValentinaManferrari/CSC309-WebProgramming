from asyncio.windows_events import NULL
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your forms here.

class NewUserForm(UserCreationForm):
	# UserCreationForm
	email = forms.EmailField(required=False)
	first_name = forms.CharField(label=_("First name"), max_length=120, required=False)
	last_name = forms.CharField(label=_("Last name"), max_length=120, required=False)

	error_messages = {
        'password_mismatch': "The two password fields didn't match",
    }

	class Meta:
		model = User
		fields = ("username", "password1", "password2", "email", "first_name", "last_name")
		error_messages = {
			'username': {
                'unique': "A user with that username already exists",
				'required': "This field is required",
            },
			'password1': {
				'min_length': "This password is too short. It must contain at least 8 characters",
				'required': "This field is required",
            },
			'password2': {
				'required': "This field is required",
            },
			'email':{
				'invalid': "Enter a valid email address",
			}
		}

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user

# # # # # PROFILERS # # # # #

class EditUserForm(forms.ModelForm):
	email = forms.EmailField(required=False)
	first_name = forms.CharField(label=_("First name"), max_length=120, required=False)
	last_name = forms.CharField(label=_("Last name"), max_length=120, required=False)
	password1 = forms.CharField(widget=forms.PasswordInput, required=False)
	password2 = forms.CharField(widget=forms.PasswordInput, required=False)
	
	error_messages = {
        'password_mismatch': "The two password fields didn't match",
    }
	
	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "password1", "password2")
		error_messages = {
			'password1': {
				'min_length': "This password is too short. It must contain at least 8 characters",
			},
			'email':{
				'invalid': "Enter a valid email address",
			}
		}

	def clean(self):
		data = super().clean()
		
		if len(data.get('password1')) > 0:
			if len(data.get('password1')) < 8:
				self.add_error('password1', 'This password is too short. It must contain at least 8 characters')
			if data.get('password1') != data.get('password2'):
				self.add_error('password2', "The two password fields didn't match")

	def save(self, commit=True):
		user = super(EditUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user