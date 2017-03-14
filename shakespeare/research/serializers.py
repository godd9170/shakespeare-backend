from rest_framework import serializers
from research.models import Company, Individual, Research, Piece, Nugget, NuggetWrapper
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

class NuggetWrapperSerializer(serializers.RelatedField):
    def get_queryset(self, values):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SELF: {}'.format(self))
        print('VALUES: {}'.format(values))
        # print('KWARGS: {}'.format(kwargs))
        return NuggetWrapper.objects.filter(mergefields__contained_by=['django'])

    # def to_representation(self, value):
    #     print('VALUE {}'.format(value))
    #     return NuggetWrapper.objects.filter(mergefields__contained_by=['django'])

    class Meta:
        model = NuggetWrapper
        fields = ('id', 'wrapper')

class NuggetSerializer(serializers.ModelSerializer):
    wrappers = NuggetWrapperSerializer(many=True)

    class Meta:
        model = Nugget
        fields = ('id', 'created', 'speaker', 'body', 'wrappers')

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
