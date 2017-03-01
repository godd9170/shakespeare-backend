from django.contrib import admin
from .models import Account, AccountUser
from organizations.models import (Organization, OrganizationUser, OrganizationOwner)

# Register your models here.
admin.site.register(Account)
admin.site.register(AccountUser)

# Unregister the generic Orgs and use the proxies
admin.site.unregister(Organization)
admin.site.unregister(OrganizationUser)
admin.site.unregister(OrganizationOwner)