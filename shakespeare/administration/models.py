from organizations.models import Organization, OrganizationUser


class Account(Organization):
    class Meta:
        proxy = True


class AccountUser(OrganizationUser):
    class Meta:
        proxy = True

    def __unicode__(self):
        return u"{0} ({1})".format(self.name if self.user.is_active and self.name
                                   else self.user.email, self.organization.name)
