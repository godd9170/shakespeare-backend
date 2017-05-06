from django.contrib import admin
from .models import Account, AccountUser, ShakespeareUser
from organizations.models import (Organization, OrganizationUser, OrganizationOwner)

# Register your models here.
admin.site.register(Account)
admin.site.register(AccountUser)

@admin.register(ShakespeareUser)
class ShakespeareUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trialemails', 'price')
    list_display_links = ('id',)
    search_fields = ('user__email',)
    list_per_page = 20

# Unregister the generic Orgs and use the proxies
admin.site.unregister(Organization)
admin.site.unregister(OrganizationUser)
admin.site.unregister(OrganizationOwner)