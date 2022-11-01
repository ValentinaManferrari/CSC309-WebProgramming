from urllib import request
from django.shortcuts import  render, redirect
from accounts.forms import RegisterForm, EditUserForm, LoginForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.contrib.auth.models import User

def homepage(request):
	return render(request=request, template_name='accounts/home.html')

# # # # # AS SIMPLE AS AUTH # # # # #

def register_request(request):
	if request.method == "GET":
		form = RegisterForm()
		return render (request=request, template_name="accounts/register.html", context={"register_form":form})
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, "Registration successful." )
			return redirect("accounts:login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		return render (request=request, template_name="accounts/register.html", context={"register_form":form})
	
def login_request(request):
	if request.method == "GET":
		form = LoginForm()
		return render(request=request, template_name="accounts/login.html", context={"login_form":form})
	if request.method == "POST":
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return HttpResponseRedirect(f"/accounts/profile/view/")
			else:
				messages.error(request,"Username or password is invalid")
				return render (request=request, template_name="accounts/login.html", context={"login_form":form})
		else:
			messages.error(request,"Username or password is invalid")
			return render (request=request, template_name="accounts/login.html", context={"login_form":form})
	
def logout_request(request):
	if request.method == "GET":
		if request.user.is_authenticated:
			logout(request)
			messages.info(request, "You have successfully logged out.") 
		return redirect("accounts:login")

# # # # # PROFILERS # # # # #

def view_profile(request):
	if request.user.is_authenticated:
		response_data = {}
		response_data['id'] = request.user.id
		response_data['username'] = request.user.username
		response_data['email'] = request.user.email
		response_data['first_name'] = request.user.first_name
		response_data['last_name'] = request.user.last_name
		return JsonResponse(response_data)
	else:
		return HttpResponse('Unauthorized', status=401)

def edit_profile(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			form = EditUserForm(data=request.POST, instance=request.user)
			if form.is_valid():
				user = form.save()
				password = form.cleaned_data.get('password1')
				if password:
					user.set_password(password) 
					user.save()
					login(request, user)
				messages.success(request, 'Your profile is updated successfully')
				return HttpResponseRedirect(f"/accounts/profile/view/")
		else:
			form = EditUserForm(instance=request.user)
	else:
		return HttpResponse('Unauthorized', status=401)
	return render(request, 'accounts/edit.html', {'edit_form': form})