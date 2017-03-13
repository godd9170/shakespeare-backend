from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^personas/$', 
        views.PersonaList.as_view(),
        name='persona-list'), #function based -> url(r'^$', views.snippet_list),
    url(r'^personas/(?P<pk>[0-9]+)/$', 
        views.PersonaDetail.as_view(),
        name='persona-detail'),
    url(r'^valueprops/$', 
        views.ValuePropositionList.as_view(),
        name='value-proposition-list'),
    url(r'^valueprops/(?P<pk>[0-9]+)$', 
        views.ValuePropositionDetail.as_view(),
        name='value-proposition-detail'),
    url(r'^ctas/$', 
        views.CallToActionList.as_view(),
        name='call-to-action-list'),
    url(r'^ctas/(?P<pk>[0-9]+)$', 
        views.CallToActionDetail.as_view(),
        name='call-to-action-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns) #support file suffix formatting