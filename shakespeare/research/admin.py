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


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'sector')
    list_display_links = ('domain',)
    search_fields = ('domain', 'name')
    list_per_page = 20

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'link_individual', 'piece_count')
    list_display_links = ('id',)
    search_fields = ('owner__name', 'individual__name')
    list_per_page = 20

    # Cross Object Links
    def link_individual(self, obj):
        if obj.individual_id is not None:
            link=urlresolvers.reverse("admin:research_individual_change", args=[obj.individual_id]) #model name has to be lowercase
            return u'<a href="%s">%s</a>' % (link,obj.individual)
    link_individual.allow_tags = True

        # Cross Object Links
    def piece_count(self, obj):
        return Piece.objects.filter(research=obj.id).count()


admin.site.register(Piece)
admin.site.register(Nugget)
admin.site.register(NuggetTemplate)