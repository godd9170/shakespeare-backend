from research.models import Research
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
        research = Research(owner=self.request.user, **utils.whois(data['email'])) #HERE WE KICK OF RESEARCH JOBS
        research.save()
        return Response({'id' : str(research.id)})
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    