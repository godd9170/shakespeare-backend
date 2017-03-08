from django.contrib import admin
from .models import Company, Individual, Research, Piece, Nugget

admin.site.register(Company)
admin.site.register(Individual)
admin.site.register(Research)
admin.site.register(Piece)
admin.site.register(Nugget)