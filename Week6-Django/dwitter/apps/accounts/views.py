from django.shortcuts import render
# ADDITION: import utility functions for creating your views
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from dwitter.apps.accounts.forms import RegistrationForm
# ADDITION: import your extended UserCreationForm
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})

# ADDITION: Create a view for the SingUpForm that you extended from UserCreationForm in forms.py