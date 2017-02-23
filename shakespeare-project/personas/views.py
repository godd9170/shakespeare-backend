from personas.models import Persona
from personas.serializers import PersonaSerializer
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, permissions # for the generic user api
from personas.permissions import IsOwner #get our specially designed permissions for the personas

class PersonaList(generics.ListCreateAPIView): #NOTE: Using the list generic
    permission_classes = (IsOwner,)
    """
    List all personas, or create a new persona.
    """
    serializer_class = PersonaSerializer

    def get_queryset(self):
        return Persona.objects.filter(owner=self.request.user) #Only show the user objects they are owners of
    # def get(self, request, format=None):
    #     personas = Persona.objects.filter(owner=self.request.user) #only show your own personas
    #     #CHECK IF USER HAS PERMISSION TO SEE THE OBJECTS (TODO: A loop?)
    #     for persona in personas:
    #         self.check_object_permissions(self.request, persona)

    #     serializer = PersonaSerializer(personas, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = PersonaSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(owner=self.request.user) #Because I'm not using the generic ModelViewSet, we need to include the owner in the save here instead of doing the overridden (perform_create)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    """
    Retrieve, update or delete a persona instance.
    """
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    # def get_object(self, pk):
    #     try:
    #         return Persona.objects.get(pk=pk)
    #     except Persona.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     persona = self.get_object(pk)
    #     self.check_object_permissions(self.request, persona) #Ensure the user has permission to see
    #     serializer = PersonaSerializer(persona)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     persona = self.get_object(pk)
    #     self.check_object_permissions(self.request, persona) #Ensure the user has permission to see this
    #     serializer = PersonaSerializer(persona, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     persona = self.get_object(pk)
    #     self.check_object_permissions(self.request, persona) #Ensure the user has permission to see this
    #     persona.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)