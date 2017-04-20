from django.core.management.base import BaseCommand
from research.models import NuggetTemplate
from .data.nuggettemplates import TEMPLATES


class Command(BaseCommand):

    def handle(self, *args, **options):
        for nugget in TEMPLATES:
            #check to see if the template already exists. #NOTE: Any small changes made within the admin
            #console will be enough to warrant a new nugget template creation. 
            if (NuggetTemplate.objects.filter(segue=nugget['segue'], intro=nugget['intro'], subject=nugget['subject']).count() < 1):
                print('Creating Template: {}'.format(nugget['subject']))
                NuggetTemplate(**nugget).save()