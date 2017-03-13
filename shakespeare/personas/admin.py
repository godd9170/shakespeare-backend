from django.contrib import admin
from .models import Persona, ValueProposition, CallToAction

# Register the main models to the admin interface
admin.site.register(Persona)
admin.site.register(ValueProposition)
admin.site.register(CallToAction)
