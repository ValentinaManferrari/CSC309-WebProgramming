from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your forms here.

class NewUserForm(UserCreationForm):
	# based on the underlying User model
	email = forms.EmailField(required=False)
	first_name = forms.CharField(label=_("First name"), max_length=120, required=False)
	last_name = forms.CharField(label=_("Last name"), max_length=120, required=False)

	class Meta:
		model = User
		fields = ("username", "password1", "password2", "email", "first_name", "last_name")
	
	def clean(self):
		data = super().clean()
		if len(data.get('username')) < 4:
			self.add_error('username', 'Username must be at least 4 characters')
		if data.get('password') != data.get('password2'):
			self.add_error('password2', 'Passwords do not match')
		if User.objects.filter(username=data.get('username')).exists():
			self.add_error('username', 'Username already exists')
		return data

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		if commit:
			user.save()
		return user