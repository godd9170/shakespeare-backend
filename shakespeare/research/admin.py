from django.contrib import admin
from django.core import urlresolvers
from .models import Company, Individual, Research, Piece, Nugget, NuggetTemplate

@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('email', 'firstname', 'lastname', 'jobtitle', 'link_company')
    list_display_links = ('email',)
    search_fields = ('email', 'firstname', 'lastname', 'company__name')
    list_per_page = 20

    # Cross Object Links
    def link_company(self, obj):
        if obj.company_id is not None:
            link=urlresolvers.reverse("admin:research_company_change", args=[obj.company_id]) #model name has to be lowercase
            return u'<a href="%s">%s</a>' % (link,obj.company)
    link_company.allow_tags = True

admin.site.register(Company)
admin.site.register(Research)
admin.site.register(Piece)
admin.site.register(Nugget)
admin.site.register(NuggetTemplate)