from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User, Group
from .models import Account, AccountUser, ShakespeareUser
from research.models import Research, Piece
from personas.models import ValueProposition
from emails.models import Email
from organizations.models import (Organization, OrganizationUser, OrganizationOwner)

# Register your models here.
# admin.site.register(Account)
# admin.site.register(AccountUser)

@admin.register(ShakespeareUser)
class ShakespeareUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'trialemails', 'price', 'research_performed', 'emails_sent', 'research_to_emails', 'vp_count', 'emails_per_day', 'pieces_per_research', 'date_joined', 'last_activity')
    list_display_links = ('email',)
    search_fields = ('user__email',)
    list_per_page = 20

    def email(self, obj):
        return obj.user.email

    def research_performed(self, obj):
        return Research.objects.filter(owner=obj.user.id).count()

    def emails_sent(self, obj):
        return Email.objects.filter(owner=obj.user.id).count()

    def date_joined(self, obj):
        return obj.user.date_joined

    def last_activity(self, obj):
        return Research.objects.filter(owner=obj.user.id).latest('created').created

    def vp_count(self, obj):
        return ValueProposition.objects.filter(owner=obj.user.id).count()

    def emails_per_day(self, obj):
        total_emails = Email.objects.filter(owner=obj.user.id).count()
        days_joined = (timezone.now() - obj.user.date_joined).days
        try:
            return total_emails/days_joined
        except ZeroDivisionError:
            return total_emails

    def pieces_per_research(self, obj):
        total_research = Research.objects.filter(owner=obj.user.id).count()
        total_pieces = Piece.objects.filter(research__owner=obj.user.id).count()
        try:
            return total_pieces/total_research
        except ZeroDivisionError:
            return total_pieces

    def research_to_emails(self, obj):
        total_research = Research.objects.filter(owner=obj.user.id).count()
        total_emails = Email.objects.filter(owner=obj.user.id).count()
        try:
            return total_research/total_emails
        except ZeroDivisionError:
            return total_research



# @admin.register(Research)
# class ResearchAdmin(admin.ModelAdmin):
#     list_display = ('id', 'owner', 'link_individual', 'piece_count')
#     list_display_links = ('id',)
#     search_fields = ('owner__name', 'individual__name')
#     list_per_page = 20

#     # Cross Object Links
#     def link_individual(self, obj):
#         if obj.individual_id is not None:
#             link=urlresolvers.reverse("admin:research_individual_change", args=[obj.individual_id]) #model name has to be lowercase
#             return u'<a href="%s">%s</a>' % (link,obj.individual)
#     link_individual.allow_tags = True



# Unregister the generic Orgs and use the proxies
admin.site.unregister(Organization)
admin.site.unregister(OrganizationUser)
admin.site.unregister(OrganizationOwner)
#admin.site.unregister(User)
admin.site.unregister(Group)