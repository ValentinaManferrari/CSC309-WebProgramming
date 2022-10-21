"""dwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from dwitter.apps.accounts import views as accounts_views  # ADDITION: import accounts_views
from dwitter.apps.tweets import views as tweets_views  # ADDITION: import tweets_views

urlpatterns = [
    # ADDITION: link admin site to the admin/ path
    # ADDITION: include the default auth urls to accounts/ path
    # ADDITION: add the signup url to accounts/signup/ path
    # ADDITION: add the index url to the root path
]
