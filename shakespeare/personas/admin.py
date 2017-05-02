from django.contrib import admin
from .models import Persona, ValueProposition, CallToAction


@admin.register(ValueProposition)
class ValuePropositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'owner', 'active', 'created')
    list_display_links = ('title',)
    search_fields = ('title', 'owner__first_name', 'owner__last_name')
    list_per_page = 20

@admin.register(CallToAction)
class CallToActionAdmin(admin.ModelAdmin):
    list_display = ('title', 'body', 'owner', 'active', 'created')
    list_display_links = ('title',)
    search_fields = ('title', 'owner__first_name', 'owner__last_name')
    list_per_page = 20

# Register the main models to the admin interface
admin.site.register(Persona)
