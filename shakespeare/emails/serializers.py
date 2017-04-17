from rest_framework import serializers
from .models import Email
from django.contrib.auth.models import User

class EmailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Email
        fields = ('id', 'subject')