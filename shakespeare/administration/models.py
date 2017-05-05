from organizations.models import Organization, OrganizationUser
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class ShakespeareUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trialemails = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    @receiver(post_save, sender=User)
    def create_shakespeare_user(sender, instance, created, **kwargs):
        if created:
            ShakespeareUser.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_shakespeare_user(sender, instance, **kwargs):
        instance.shakespeareuser.save()


class Account(Organization):
    class Meta:
        proxy = True


class AccountUser(OrganizationUser):
    class Meta:
        proxy = True

    def __unicode__(self):
        return u"{0} ({1})".format(self.name if self.user.is_active and self.name
                                   else self.user.email, self.organization.name)

