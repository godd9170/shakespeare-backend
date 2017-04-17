from django.core.management.base import BaseCommand
from research.models import NuggetTemplate
from .data.nuggettemplates import TEMPLATES


class Command(BaseCommand):

    def handle(self, *args, **options):
        if (NuggetTemplate.objects.all().count() < 1):
            for nugget in TEMPLATES:
                NuggetTemplate(**nugget).save()