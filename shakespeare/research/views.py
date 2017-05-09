from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from emails.models import Email

from .models import Research, Individual
from .serializers import ResearchSerializer
from .tasks import collect_research
from .exceptions import UserMustPayException
from . import utils


class ResearchDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, uuid):
        try:
            return Research.objects.get(pk=uuid)
        except Research.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        research = self.get_object(uuid)
        serializer = ResearchSerializer(research)
        return Response(serializer.data)

    def valid_trial_or_payment(self):
        request = self.request
        if not hasattr(request.user, 'customer') and (Email.objects.filter(owner=request.user).count() >= request.user.shakespeareuser.trialemails):
            raise UserMustPayException


    def post(self, request, format=None):
        data = request.data
        self.valid_trial_or_payment() #check that the user isn't past their trial limit.
        # 
        # Get the person we're dealing with
        #
        if ('individualObject' not in data): # If the first name not supplied in the request, go try to find the individual normally via the database or Clearbit
            email = data['email']
            try:  # See if we have this individual already
                individual = Individual.objects.get(email=email)
                if individual.modified < (timezone.now() - timedelta(days=settings.INDIVIDUAL_REFRESH_MAX_AGE)):
                    individual = utils.update_individual(email)
            except ObjectDoesNotExist:
                # We don't have this individual, let's get Clearbit to try
                individual = utils.create_individual(email)
        else : # If Clearbit was no good, create an individual and company and perform research based on the user-supplied information
            individual = utils.create_individual_without_clearbit(data['individualObject'], data['companyObject'])
        
        # 
        # Create a new research 
        #
        research = Research(individual=individual, owner=self.request.user) 
        research.save()
        # 
        # Aggregate some sources for this person

        collect_research(research)

        return Response({'id': str(research.id)})
            