from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from personas import views

urlpatterns = [
    url(r'^$', views.PersonaList.as_view()), #function based -> url(r'^$', views.snippet_list),
    url(r'^(?P<pk>[0-9]+)/$', views.PersonaDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns) #support file suffix formatting