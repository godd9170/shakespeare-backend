from social_core.backends.google import GooglePlusAuth
from social_core.backends.utils import load_backends
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from personas.models import ValueProposition, CallToAction
from .data.defaults import DEFAULT_CALLS_TO_ACTION  #, DEFAULT_VALUE_PROPOSITIONS 



# Create and initialize a new user
def create_user(email):
    try:  # See if we've got this user already
        user = User.objects.get(email=email)
    except ObjectDoesNotExist:
        # We don't have this user, let's make 'em
        user = User.objects.create_user(
            username=email,
            email=email
        )
        # #make the vps
        # for vp in DEFAULT_VALUE_PROPOSITIONS:
        #     ValueProposition(owner=user, **vp).save()

        #make the ctas
        for cta in DEFAULT_CALLS_TO_ACTION:
            CallToAction(owner=user, **cta).save()
    return



def is_authenticated(user):
    if callable(user.is_authenticated):
        return user.is_authenticated()
    else:
        return user.is_authenticated


def associations(user, strategy):
    user_associations = strategy.storage.user.get_social_auth_for_user(user)
    if hasattr(user_associations, 'all'):
        user_associations = user_associations.all()
    return list(user_associations)


def common_context(authentication_backends, strategy, user=None, plus_id=None, **extra):
    """Common view context"""
    context = {
        'user': user,
        'available_backends': load_backends(authentication_backends),
        'associated': {}
    }

    if user and is_authenticated(user):
        context['associated'] = dict((association.provider, association)
                                     for association in associations(user, strategy))

    if plus_id:
        context['plus_id'] = plus_id
        context['plus_scope'] = ' '.join(GooglePlusAuth.DEFAULT_SCOPE)

    return dict(context, **extra)


def url_for(name, **kwargs):
    if name == 'social:begin':
        url = '/login/{backend}/'
    elif name == 'social:complete':
        url = '/complete/{backend}/'
    elif name == 'social:disconnect':
        url = '/disconnect/{backend}/'
    elif name == 'social:disconnect_individual':
        url = '/disconnect/{backend}/{association_id}/'
    else:
        url = name
    return url.format(**kwargs)
