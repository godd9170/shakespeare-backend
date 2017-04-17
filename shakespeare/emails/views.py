from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.apps import apps
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Email
from research.models import Nugget
from personas.models import ValueProposition, CallToAction
from .serializers import EmailSerializer

class EmailDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, id, appName, modelName):
        if id is not None:
            Model = apps.get_model(app_label=appName, model_name=modelName)
            try:
                return Model.objects.get(pk=id)
            except Model.DoesNotExist:
                raise Http404
        else:
            return None

    def get(self, request, uuid, format=None):
        email = self.get_object(uuid, 'emails', 'Email')
        serializer = EmailSerializer(email)
        return Response(serializer.data)

    def post(self, request, format=None):
        """
        Records all of the details of a given email sent with shakespeare. Expecting a
        payload that looks like this:
        {
            "gmailid" : "15b688c6aa471d68", #Uniquely generated gmail id
            "selectednugget" : 1, #The id of the last nugget selected
            "selectedvalueproposition" : 1, #The id of the last value prop selected
            "selectedcalltoaction" : 1, #The id of the last selected cta
            "emailto" : "hgoddard@saasli.com", #The email of the recipient (should match the individual id TODO: LINK TO THE ACTUAL INDIVIDUAL MODEL)
            "emailcc" : ["hgoddard@saasli.com", "ggoddard@saasli.com"],
            "emailbcc" : ["hgoddard@saasli.com", "ggoddard@saasli.com"],
            "subject" : "Open this damn email!",
            "body" : "Can you tell me why you opened this damn email?",
            "salutation" : "Hello Dummy,",
            "introduction" : "Ha! I can't believe you opened this damn email!",
            "valueproposition" : "We help get people to open your damn emails.",
            "calltoaction" : "Reply, and I'll open your damn email.",
            "signature" : "Signed, Hank"
        }
        """
        data = request.data
        nugget = self.get_object(data.pop('selectednugget', None), 'research', 'Nugget')
        valueprop = self.get_object(data.pop('selectedvalueproposition', None), 'personas', 'ValueProposition')
        calltoaction = self.get_object(data.pop('selectedcalltoaction', None), 'personas', 'CallToAction')
        email = Email(
            owner=self.request.user, 
            selectednugget=nugget,
            selectedvalueproposition=valueprop,
            selectedcalltoaction=calltoaction,
            **data
        )
        email.save()
        return Response({'id': str(email.id)})
