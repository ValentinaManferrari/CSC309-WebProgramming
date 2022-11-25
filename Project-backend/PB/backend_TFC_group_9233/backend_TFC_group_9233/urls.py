"""backend_TFC_group_9233 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.i18n import JavaScriptCatalog

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('classes/', include('classes.urls', namespace='classes')),
    path('studios/', include('studios.urls', namespace='studios')), 
    path('subscriptions/', include('subscriptions.urls', namespace='subscriptions')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # If you already have a js_info_dict dictionary, just add
# # 'recurrence' to the existing 'packages' tuple.
# js_info_dict = {
#     'packages': ('recurrence', ),
# }
# # jsi18n can be anything you like here
# urlpatterns += [
#     re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), js_info_dict),
# ]