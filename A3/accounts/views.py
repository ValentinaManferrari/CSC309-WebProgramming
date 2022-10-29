from django.shortcuts import  render, redirect
from accounts.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

def homepage(request):
	return render(request=request, template_name='accounts/home.html')

def register_request(request):
	if request.method == "GET":
		form = NewUserForm()
		return render (request=request, template_name="accounts/register.html", context={"register_form":form})
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("accounts:login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
		return render (request=request, template_name="accounts/register.html", context={"register_form":form})
	
	
def login_request(request):
	if request.method == "GET":
		form = AuthenticationForm()
		return render(request=request, template_name="accounts/login.html", context={"login_form":form})

	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("accounts:homepage") # to redirect later
			else:
				messages.error(request,"Invalid username or password.")
				return redirect("accounts:homepage")
		else:
			messages.error(request,"Invalid username or password.")
			return redirect("accounts:homepage")
	
def logout_request(request):
	if request.method == "GET":
		logout(request)
		messages.info(request, "You have successfully logged out.") 
		return redirect("accounts:login")