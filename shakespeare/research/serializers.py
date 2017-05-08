from rest_framework import serializers
from research.models import Company, Individual, Research, Piece, Nugget, NuggetTemplate
from django.contrib.auth.models import User

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ( 'domain', 'created', 'name', 'cleanedname', 'industry', 'sector', 'crunchbase', 'description', 'logo')

class IndividualSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Individual
        fields = ( 'email', 'created', 'firstname', 'lastname', 'jobtitle', 'role', 'avatar', 'company', 'companyname', 'linkedinhandle')


class NuggetSerializer(serializers.ModelSerializer):
    compositions = serializers.SerializerMethodField()

    def get_compositions(self, nugget):
        mergefields = list(nugget.get_mergefields()) #Get all the additional data merge fields
        templates = NuggetTemplate.objects.filter(mergefields__contained_by = mergefields, category = nugget.category)
        return NuggetTemplateSerializer(templates, many=True, context={'nugget' : nugget}).data

    class Meta:
        model = Nugget
        fields = ('id', 'created', 'category', 'body', 'compositions', 'additionaldata')

class NuggetTemplateSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    intro = serializers.SerializerMethodField()
    segue = serializers.SerializerMethodField()

    def get_subject(self, nuggettemplate):
        return nuggettemplate.merge(nuggettemplate.subject, self.context['nugget'])

    def get_intro(self, nuggettemplate):
        return nuggettemplate.merge(nuggettemplate.intro, self.context['nugget'])

    def get_segue(self, nuggettemplate):
        return nuggettemplate.merge(nuggettemplate.segue, self.context['nugget'])

    class Meta:
        model = NuggetTemplate
        fields = ('subject', 'intro', 'segue')

class PieceSerializer(serializers.ModelSerializer):
    nuggets = NuggetSerializer(many=True, source='nugget', read_only=True)

    class Meta:
        model = Piece
        fields = ('id', 'title', 'body', 'author', 'aggregator', 'publisheddate', 'created', 'source', 'group', 'nuggets', 'url')

class ResearchSerializer(serializers.ModelSerializer):
    pieces = PieceSerializer(many=True, source='piece', read_only=True)
    individual = IndividualSerializer(read_only=True)

    class Meta:
        model = Research
        fields = ('id', 'created', 'individual', 'complete', 'pieces')
