from rest_framework import serializers
from personas.models import Persona
from django.contrib.auth.models import User
from personas.models import ValueProposition, CallToAction

class PersonaSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') #You can include additional fields that aren't necessarily on the model like this
    calls_to_action = serializers.PrimaryKeyRelatedField(many=True, queryset=CallToAction.objects.all())
    value_propositions = serializers.PrimaryKeyRelatedField(many=True, queryset=ValueProposition.objects.all())
    
    class Meta:
        model = Persona
        fields = ('id', 'title', 'owner', 'calls_to_action', 'value_propositions')

class ValuePropositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ValueProposition
        fields = ('id', 'title', 'persona')

class CallToActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CallToAction
        fields = ('id', 'title', 'persona')