from social_core.pipeline.partial import partial


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email: #is there an email (or is this an ajax request)? we're good if so.
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email') 
        if email:
            details['email'] = email
        else:
            current_partial = kwargs.get('current_partial')
            return strategy.redirect(
                '/email?partial_token={0}'.format(current_partial.token) #if there is no email, tell the user they're out of luck
            )