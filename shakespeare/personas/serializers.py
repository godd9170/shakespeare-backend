from rest_framework import serializers
from personas.models import Persona, ValueProposition, CallToAction
from django.contrib.auth.models import User

class ValuePropositionSerializer(serializers.HyperlinkedModelSerializer):
    personas = serializers.HyperlinkedRelatedField(many=True, view_name='persona-detail', queryset=Persona.objects.all())

    class Meta:
        model = ValueProposition
        fields = ('id', 'title', 'personas')

class CallToActionSerializer(serializers.HyperlinkedModelSerializer):
    personas = serializers.HyperlinkedRelatedField(many=True, view_name='persona-detail', queryset=Persona.objects.all())

    class Meta:
        model = CallToAction
        fields = ('id', 'title', 'personas')

class PersonaSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') #You can include additional fields that aren't necessarily on the model like this
    value_propositions = ValuePropositionSerializer(many=True, source='value_proposition_personas', read_only=True)
    calls_to_action = CallToActionSerializer(many=True, source='call_to_action_personas', read_only=True)

    class Meta:
        model = Persona
        fields = ('id', 'title', 'owner' , 'value_propositions', 'calls_to_action')