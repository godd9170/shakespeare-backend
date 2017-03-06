from django.conf.urls import url, include
from administration import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^email-sent/', views.validation_sent),
    url(r'^login/$', views.home),
    url(r'^logout/$', views.logout),
    url(r'^done/$', views.done, name='done'),
    url(r'^ajax-auth/(?P<backend>[^/]+)/$', views.ajax_auth,
        name='ajax-auth'),
    url(r'^email/$', views.require_email, name='require_email'),
    url(r'', include('social_django.urls'))
]