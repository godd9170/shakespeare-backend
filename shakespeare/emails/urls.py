from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', 
        views.EmailDetail.as_view(),
        name='create_email'),
    url(r'^(?P<uuid>[^/]+)/$', 
        views.EmailDetail.as_view(),
        name='detail_email')
]