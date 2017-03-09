from research.models import Research, Individual, Company
from django.core.exceptions import ObjectDoesNotExist
from research.serializers import ResearchSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from research import utils
import json

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

        try: # See if we've got this individual already
            individual = Individual.objects.get(email=email) 
        except ObjectDoesNotExist: # We don't have this individual, let's get Clearbit to try
            individual = utils.whois(email) #this will toss an API error if nobody is found # create the research
        
        research = Research(individual=individual, owner=self.request.user) #HERE WE KICK OF RESEARCH JOBS
        research.save()
        return Response({'id' : str(research.id)})
    
    