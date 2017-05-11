from django.contrib import admin
from django.core import urlresolvers
from .models import Email


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'emailto', 'link_selectednugget', 'link_selectedvalueproposition', 'link_selectedcalltoaction', 'created')
    list_display_links = ('id',)
    search_fields = ('emailto', 'owner__email', 'owner__username')
    list_per_page = 20
    raw_id_fields = ( # don't do a dropdown
        'selectednugget',
        'selectedvalueproposition',
        'selectedcalltoaction'
    )

    # Cross Object Links
    def link_selectednugget(self, obj):
        if obj.selectednugget_id is not None:
            link=urlresolvers.reverse("admin:research_nugget_change", args=[obj.selectednugget_id]) #model name has to be lowercase
            return u'<a href="%s">%s</a>' % (link,obj.selectednugget)
    link_selectednugget.allow_tags = True

    def link_selectedvalueproposition(self, obj):
        if obj.selectedvalueproposition_id is not None:
            link=urlresolvers.reverse("admin:personas_valueproposition_change", args=[obj.selectedvalueproposition_id]) #model name has to be lowercase
            return u'<a href="%s">%s</a>' % (link,obj.selectedvalueproposition)
    link_selectedvalueproposition.allow_tags = True

    def link_selectedcalltoaction(self, obj):
        if obj.selectedcalltoaction_id is not None:
            link=urlresolvers.reverse("admin:personas_calltoaction_change", args=[obj.selectedcalltoaction_id]) #model name has to be lowercase
            return u'<a href="%s">%s</a>' % (link,obj.selectedcalltoaction)
    link_selectedcalltoaction.allow_tags = True


# EG:
# class DecadeBornListFilter(admin.SimpleListFilter):
#     # Human-readable title which will be displayed in the
#     # right admin sidebar just above the filter options.
#     title = _('decade born')

#     # Parameter for the filter that will be used in the URL query.
#     parameter_name = 'decade'

#     def lookups(self, request, model_admin):
#         """
#         Returns a list of tuples. The first element in each
#         tuple is the coded value for the option that will
#         appear in the URL query. The second element is the
#         human-readable name for the option that will appear
#         in the right sidebar.
#         """
#         return (
#             ('80s', _('in the eighties')),
#             ('90s', _('in the nineties')),
#         )

#     def queryset(self, request, queryset):
#         """
#         Returns the filtered queryset based on the value
#         provided in the query string and retrievable via
#         `self.value()`.
#         """
#         # Compare the requested value (either '80s' or '90s')
#         # to decide how to filter the queryset.
#         if self.value() == '80s':
#             return queryset.filter(birthday__gte=date(1980, 1, 1),
#                                     birthday__lte=date(1989, 12, 31))
#         if self.value() == '90s':
#             return queryset.filter(birthday__gte=date(1990, 1, 1),
#                                     birthday__lte=date(1999, 12, 31))

# class PersonAdmin(admin.ModelAdmin):
#     list_filter = (DecadeBornListFilter,)