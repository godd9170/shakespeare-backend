from social_core.pipeline.partial import partial
import rollbar


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

def reject_user_if_non_existent(strategy, details, user=None, is_new=False, *args, **kwargs):
    if user is None:
        # We want to know if someone can't get in.
        rollbar.report_message(
            '[Invalid User Login Attempt] Someone has attempted to access the system with an invalid google account.', 
            'warning', 
            extra_data={'fullname' : details['fullname'], 'email' : details['email'] }
        )
        print('REJECTING USER: {}'.format(details))
        return strategy.redirect('/administration/invite-only/?email={}'.format(details['email']))
