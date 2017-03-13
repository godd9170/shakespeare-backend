from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', 
        views.ResearchDetail.as_view(),
        name='create_research'),
    url(r'^(?P<uuid>[^/]+)/$', 
        views.ResearchDetail.as_view(),
        name='detail_research'),
]