from rest_framework import generics  # for the generic user api
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import models, serializers, permissions



@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'personas': reverse('persona-list', request=request, format=format),
        'valueprops': reverse('value-proposition-list', request=request, format=format),
        'ctas': reverse('call-to-action-list', request=request, format=format),
    })


class PersonaList(generics.ListCreateAPIView):  # NOTE: Using the list generic
    permission_classes = (permissions.IsOwner,)
    """
    List all personas, or create a new persona.
    """
    serializer_class = serializers.PersonaSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return models.Persona.objects.filter(owner=self.request.user)  #Only show the user objects they are owners of


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsOwner,)
    """
    Retrieve, update or delete a persona instance.
    """
    queryset = models.Persona.objects.all()
    serializer_class = serializers.PersonaSerializer


class ValuePropositionList(generics.ListCreateAPIView):  # NOTE: Using the list generic
    """
    List all personas, or create a new persona.
    """
    serializer_class = serializers.ValuePropositionSerializer

    def get_queryset(self):
        # return models.ValueProposition.objects.all()
        return models.ValueProposition.objects.filter(owner=self.request.user) #Only show the user objects they are owners of

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ValuePropositionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a persona instance.
    """
    queryset = models.ValueProposition.objects.all()
    serializer_class = serializers.ValuePropositionSerializer



class CallToActionList(generics.ListCreateAPIView):  # NOTE: Using the list generic
    """
    List all personas, or create a new persona.
    """
    serializer_class = serializers.CallToActionSerializer

    def get_queryset(self):
        # return models.CallToAction.objects.all()
        return models.CallToAction.objects.filter(owner=self.request.user) #Only show the user objects they are owners of

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CallToActionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a persona instance.
    """
    queryset = models.CallToAction.objects.all()
    serializer_class = serializers.CallToActionSerializer

