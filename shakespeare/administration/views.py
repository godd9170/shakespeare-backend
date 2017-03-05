import json
from .decorators import render_to

# Django Stuff
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login, get_user_model

# Social Auth Stuff
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
#from social.exceptions import AuthAlreadyAssociated
from social_django.utils import psa, load_strategy

# Django Rest Framework Stuff
from rest_framework import status
from rest_framework.response import Response


User = get_user_model()

#Thanks https://yeti.co/blog/social-auth-with-django-rest-framework/
# class SocialSignUp(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = SocialSignUpSerializer
#     # This permission is nothing special, see part 2 of this series to see its entirety
#     permission_classes = (IsAuthenticatedOrCreate,) #TODO Investigate

#     def create(self, request, *args, **kwargs):
#         """
#         Override `create` instead of `perform_create` to access request
#         request is necessary for `load_strategy`
#         """
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         provider = request.data['provider']

#         # If this request was made with an authenticated user, try to associate this social 
#         # account with it
#         authed_user = request.user if not request.user.is_anonymous() else None

#         # `strategy` is a python-social-auth concept referencing the Python framework to
#         # be used (Django, Flask, etc.). By passing `request` to `load_strategy`, PSA 
#         # knows to use the Django strategy
#         strategy = load_strategy(request)
#         # Now we get the backend that corresponds to our user's social auth provider
#         # e.g., Facebook, Twitter, etc.
#         backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)

#         if isinstance(backend, BaseOAuth1): # This won't happen
#             # Twitter, for example, uses OAuth1 and requires that you also pass
#             # an `oauth_token_secret` with your authentication request
#             token = {
#                 'oauth_token': request.data['access_token'],
#                 'oauth_token_secret': request.data['access_token_secret'],
#             }
#         elif isinstance(backend, BaseOAuth2):
#             # We're using oauth's implicit grant type (usually used for web and mobile 
#             # applications), so all we have to pass here is an access_token
#             token = request.data['access_token']

#         try:
#             # if `authed_user` is None, python-social-auth will make a new user,
#             # else this social account will be associated with the user you pass in
#             user = backend.do_auth(token, user=authed_user)
#         except AuthAlreadyAssociated:
#             # You can't associate a social account with more than user
#             return Response({"errors": "That social media account is already in use"},
#                             status=status.HTTP_400_BAD_REQUEST)

#         if user and user.is_active:
#             # if the access token was set to an empty string, then save the access token 
#             # from the request
#             auth_created = user.social_auth.get(provider=provider)
#             if not auth_created.extra_data['access_token']:
#                 # Facebook for example will return the access_token in its response to you. 
#                 # This access_token is then saved for your future use. However, others 
#                 # e.g., Instagram do not respond with the access_token that you just 
#                 # provided. We save it here so it can be used to make subsequent calls.
#                 auth_created.extra_data['access_token'] = token
#                 auth_created.save()

#             # Set instance since we are not calling `serializer.save()`
#             serializer.instance = user
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, 
#                             headers=headers)
#         else:
#             return Response({"errors": "Error with social authentication"},
#                             status=status.HTTP_400_BAD_REQUEST)

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')


@render_to('home.html')
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')


@login_required
@render_to('home.html')
def done(request):
    """Login complete view, displays user data"""
    pass


@render_to('home.html')
def validation_sent(request):
    """Email validation sent confirmation page"""
    return {
        'validation_sent': True,
        'email': request.session.get('email_validation_address')
    }


@render_to('home.html')
def require_email(request):
    """Email required page"""
    strategy = load_strategy()
    partial_token = request.GET.get('partial_token')
    partial = strategy.partial_load(partial_token)
    return {
        'email_required': True,
        'partial_backend_name': partial.backend,
        'partial_token': partial_token
    }


@psa('social:complete')
def ajax_auth(request, backend):
    print('Made it to ajax auth')
    """AJAX authentication endpoint"""
    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')
