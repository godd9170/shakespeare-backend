from django.conf.urls import url
from administration.views import index, auth_return


urlpatterns = [
    # Example:
    url(r'^$', index ),
    url(r'^oauth2callback', auth_return ),
]

#urlpatterns = format_suffix_patterns(urlpatterns) #support file suffix formatting