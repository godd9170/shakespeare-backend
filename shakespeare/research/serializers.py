from rest_framework import serializers
from research.models import Company, Individual, Research, Piece, Nugget, NuggetTemplate
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
    templates = serializers.SerializerMethodField()

    def get_templates(self, nugget):
        mergefields = list(nugget.get_mergefields()) #Get all the additional data merge fields
        templates = NuggetTemplate.objects.filter(mergefields__contained_by = mergefields)
        return NuggetTemplateSerializer(templates, many=True).data

    class Meta:
        model = Nugget
        fields = ('id', 'created', 'category', 'speaker', 'body', 'templates', 'additionaldata')

class NuggetTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NuggetTemplate
        fields = ('subject', 'intro', 'segue')

class PieceSerializer(serializers.ModelSerializer):
    nuggets = NuggetSerializer(many=True, source='nugget', read_only=True)

    class Meta:
        model = Piece
        fields = ('id', 'title', 'body', 'source', 'author', 'publisheddate', 'created', 'nuggets')

class ResearchSerializer(serializers.ModelSerializer):
    pieces = PieceSerializer(many=True, source='piece', read_only=True)
    individual = IndividualSerializer(read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'created', 'individual', 'complete', 'pieces')
