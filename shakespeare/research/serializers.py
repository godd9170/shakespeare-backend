from rest_framework import serializers
from research.models import Research, Piece, Nugget
from django.contrib.auth.models import User

class NuggetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nugget
        fields = ('id', 'created', 'actor', 'body' )

class PieceSerializer(serializers.ModelSerializer):
    nuggets = NuggetSerializer(many=True, source='nugget', read_only=True)

    class Meta:
        model = Piece
        fields = ('id', 'title', 'body', 'source', 'author', 'nuggets')

class ResearchSerializer(serializers.ModelSerializer):
    pieces = PieceSerializer(many=True, source='piece', read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'created', 'firstname', 'lastname' , 'jobtitle', 'avatar', 'email', 'company', 'complete', 'pieces')