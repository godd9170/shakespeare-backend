import os
import logging
import httplib2

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render

from shakespeare import settings
from administration.models import CredentialsModel

from googleapiclient.discovery import build
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage as Storage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'google_credentials.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://mail.google.com/',
    redirect_uri='http://localhost:8000/administration/oauth2callback')

@login_required
def index(request):
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid == True:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        # service = build("plus", "v1", http=http)
        # activities = service.activities()
        # activitylist = activities.list(collection='public',
        #                                userId='me').execute()
        # logging.info(activitylist)
        return HttpResponseRedirect("/") #chuck back to persona


@login_required
def auth_return(request):
    state = bytes(request.GET.get('state', '') , 'utf8') #obtain the state from the query string
    code = bytes(request.GET.get('code', '') , 'utf8') #obtain the code from the query string
    if not xsrfutil.validate_token(settings.SECRET_KEY, state, request.user):
        return  HttpResponseBadRequest()
    credential = FLOW.step2_exchange(code)
    storage = Storage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    return HttpResponseRedirect("/")