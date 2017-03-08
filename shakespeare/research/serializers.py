from rest_framework import serializers
from research.models import Company, Individual, Research, Piece, Nugget
from django.contrib.auth.models import User

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ( 'domain', 'created', 'name', 'industry', 'sector', 'crunchbase', 'description', 'logo')

class IndividualSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Individual
        fields = ( 'email', 'created', 'firstname', 'lastname', 'jobtitle', 'role', 'avatar', 'company', 'companyname')

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
    individual = IndividualSerializer(read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'created', 'individual', 'complete', 'pieces')
