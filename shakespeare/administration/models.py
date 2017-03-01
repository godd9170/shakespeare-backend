import pickle
import base64
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

from organizations.models import Organization, OrganizationUser
from oauth2client.contrib.django_util.models import CredentialsField

class Account(Organization):
    class Meta:
        proxy = True

class AccountUser(OrganizationUser):
    class Meta:
        proxy = True

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()

class CredentialsAdmin(admin.ModelAdmin):
    pass