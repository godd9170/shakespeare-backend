from organizations.models import Organization, OrganizationUser
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from .data.defaults import DEFAULT_CALLS_TO_ACTION  #, DEFAULT_VALUE_PROPOSITIONS 
from personas.models import CallToAction
from pinax.stripe.models import Plan

#Should the stripe plan ever get f***ed up, these are the defaults
DEFAULT_TRIAL_EMAILS = 10
DEFAULT_PRICE = 36

class ShakespeareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trialemails = models.IntegerField(default=DEFAULT_TRIAL_EMAILS)
    price = models.IntegerField(default=DEFAULT_PRICE)

    @receiver(post_save, sender=User)
    def create_shakespeare_user(sender, instance, created, **kwargs):
        if created:
            #set the trial amounts
            try: #try to get the trial amounts from the default plan
                default_plan_info = Plan.objects.get(stripe_id=settings.PINAX_STRIPE_DEFAULT_PLAN).metadata #get default plan info
                trialemails = int(default_plan_info.get('trialemails', DEFAULT_TRIAL_EMAILS))
                price = int(default_plan_info.get('price', DEFAULT_PRICE))
                ShakespeareUser.objects.create(
                    user=instance,
                    trialemails=trialemails,
                    price=price
                )
            except: #just use the default set in the model if we can't find a plan
                ShakespeareUser.objects.create(user=instance)
            #make the ctas
            for cta in DEFAULT_CALLS_TO_ACTION:
                CallToAction(owner=instance, **cta).save()

    @receiver(post_save, sender=User)
    def save_shakespeare_user(sender, instance, **kwargs):
        instance.shakespeareuser.save()

    def __str__(self):
        return str(self.user.email)


class Account(Organization):
    class Meta:
        proxy = True


class AccountUser(OrganizationUser):
    class Meta:
        proxy = True

    def __unicode__(self):
        return u"{0} ({1})".format(self.name if self.user.is_active and self.name
                                   else self.user.email, self.organization.name)

