from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from administration.models import ShakespeareUser


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--trialemails', type=int, default=10)
        parser.add_argument('--price', type=int, default=36)

    def handle(self, *args, **options):
        for user in User.objects.all():
            if not hasattr(user, 'shakespeareuser'): #if we don't yet have a related 1:1 we'll need to make one
                print('Creating shakespeareuser for {}'.format(user))
                ShakespeareUser(
                    user=user, 
                    trialemails=options['trialemails'],
                    price=options['price']
                ).save()