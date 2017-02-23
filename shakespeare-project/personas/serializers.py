from rest_framework import serializers
from personas.models import Persona
from django.contrib.auth.models import User

class PersonaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') #You can include additional fields that aren't necessarily on the model like this

    class Meta:
        model = Persona
        fields = ('id', 'title', 'owner')