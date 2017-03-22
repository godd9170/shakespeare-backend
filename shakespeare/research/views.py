from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone

from .models import Research, Individual
from .serializers import ResearchSerializer
from .tasks import get_research_pieces_task
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

    def post(self, request, format=None):
        data = request.data
        email = data['email']

        # 
        # Get the person we're dealing with
        #
        try:  # See if we've got this individual already
            individual = Individual.objects.get(email=email)
            if individual.modified < (timezone.now() - timedelta(days=settings.INDIVIDUAL_REFRESH_MAX_AGE)):
                # if (datetime.timedelta(datetime.datetime.now() - individual.modified) > settings.INDIVIDUAL_REFRESH_MAX_AGE):
                # if (individual.modified + settings.INDIVIDUAL_REFRESH_MAX_AGE > datetime.datetime.now()):
                individual = utils.update_individual(email)


        except ObjectDoesNotExist:
            # We don't have this individual, let's get Clearbit to try
            individual = utils.create_individual(email)

        # 
        # Create a new research 
        #
        research = Research(individual=individual, owner=self.request.user) 
        research.save()
        # 
        # Aggregate some sources for this person
        #
        #utils.get_research_pieces(research)
        # get_research_pieces_task(research_id=research.pk) #SYNC
        get_research_pieces_task.delay(research_id=research.pk) #ASYNC

        return Response({'id': str(research.id)})