from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    readonly_fields = (
        'selectednugget',
        'selectedvalueproposition',
        'selectedcalltoaction'
    )
