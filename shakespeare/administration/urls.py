from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r'^$', views.home),
    url(r'^isvalid/', views.isvalid),
    url(r'^pay/', views.pay),
    url(r'^get-started/', views.getstarted, name='getstarted'),
    url(r'^create-user/', views.createuser),
    url(r'^subscribe/', views.subscribe, name='subscribe'),
    url(r'^login/$', views.home),
    url(r'^logout/$', views.logout),
    url(r'^me/$', views.me),
    url(r'^done/$', views.done, name='done'),
    url(r'^invite-only/$', views.inviteonly, name='invite-only'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', views.ajax_auth,
        name='ajax-auth'),
    url(r'^email/$', views.require_email, name='require_email'),
    url(r'', include('social_django.urls'))
]