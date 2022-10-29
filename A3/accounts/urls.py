from django.urls import path

from accounts.views import homepage, register_request, login_request, logout_request
app_name = 'accounts'

urlpatterns = [
    path('', homepage, name="homepage"),
    path('register/', register_request, name="register"),
    path('login/', login_request, name="login"),
    path('logout/', logout_request, name= "logout"),
]
