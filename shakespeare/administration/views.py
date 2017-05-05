import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.views import View
from .decorators import render_to
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout as auth_logout, login, get_user_model
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_django.utils import psa, load_strategy
from django.conf import settings
from emails.models import Email
from pinax.stripe.models import Plan

from . import utils

@api_view(['GET'])
def isvalid(request):
    return Response(status=200)

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return redirect('/')

@render_to('administration/shakespeare.html')
def shakespeare(request):
    pass

@api_view(['GET'])
def me(request):
    user = request.user
    sent = Email.objects.filter(owner=request.user).count() #how many emails have been sent?
    return Response(
        {
            "firstname": user.first_name,
            "lastname": user.last_name,
            "sent" : sent
        }
    )




@render_to('administration/invite-only.html')
def inviteonly(request):
    pass

#@render_to('administration/get-started.html')
@csrf_exempt
def getstarted(request):
    if request.POST:
        default_plan_info = Plan.objects.get(stripe_id=settings.PINAX_STRIPE_DEFAULT_PLAN).metadata #get default plan info
        user = utils.create_user(request.POST['email']) #make or fetch the user
        print(">>>>>>>>>>>>>>>>>>>USER: {}".format(user.__dict__))
        user.shakspeareuser.trialemails = default_plan_info['trialemails']
        user.shakspeareuser.price = default_plan_info['price']
        user.save()

        customer = utils.create_stripe_customer(user, request.POST['stripeToken']) #make a new stripe user
        return render(
            request, 
            'administration/get-started.html'
        )
    else:
        return redirect('subscribe')

#@render_to('administration/subscribe.html')
def subscribe(request):
    default_plan_info = Plan.objects.get(stripe_id=settings.PINAX_STRIPE_DEFAULT_PLAN).metadata
    print(default_plan_info['price'])
    return render(
        request, 
        'administration/subscribe.html', 
        {
            'PINAX_STRIPE_PUBLIC_KEY' : settings.PINAX_STRIPE_PUBLIC_KEY,
            'SHAKESPEARE_MONTHLY_PRICE' : default_plan_info['price'],
            'SHAKESPEARE_BILLING_FREQUENCY' : default_plan_info['billing']
        }
    )

@api_view(['POST'])
@permission_classes((AllowAny, ))
def createuser(request):
    utils.create_user(request.data['form_response']['answers'][2]['email'])
    return Response(status=200)

@render_to('administration/home.html')
def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('done')


@login_required
@render_to('administration/home.html')
def done(request):
    """Login complete view, displays user data"""
    pass


@render_to('administration/home.html')
def validation_sent(request):
    """Email validation sent confirmation page"""
    return {
        'validation_sent': True,
        'email': request.session.get('email_validation_address')
    }


@render_to('administration/home.html')
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
