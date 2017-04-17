"""shakespeare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import os
from django.conf.urls import include, url
from django.contrib import admin
from administration import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.shakespeare),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^administration/', include('administration.urls')),
    url(r'^research/', include('research.urls')),
    url(r'^emails/', include('emails.urls')),
    url(r'^personas/', include('personas.urls'))
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # url(r'^accounts/', include('organizations.urls')),
    # url(r'^invitations/', include(invitation_backend().get_urls())),
]

#import newspaper
import clearbit
#from newspaper import settings as newspaper_settings
#newspaper_settings.DATA_DIRECTORY = os.path.join(settings.BASE_DIR, '.newspaper')

clearbit.key = settings.CLEARBIT_KEY