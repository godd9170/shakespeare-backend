import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField # JSON + Array Fields
from model_utils.models import TimeStampedModel
from research.models import Nugget
from personas.models import ValueProposition, CallToAction


class Email(TimeStampedModel):
    # housekeeping fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey('auth.User', related_name='emails', on_delete=models.CASCADE)
    
    # Fields to allow us to find/identify the email
    gmailid = models.TextField(blank=False) # The unique identifier of the email that was sent

    # Fields that show us what in the app was (in theory) used in this email
    selectednugget = models.ForeignKey('research.Nugget', related_name='selectednugget', null=True, on_delete=models.SET_NULL)
    selectedvalueproposition = models.ForeignKey('personas.ValueProposition', related_name='selectedvalueproposition', null=True, on_delete=models.SET_NULL)
    selectedcalltoaction = models.ForeignKey('personas.CallToAction', related_name='selectedcalltoaction', null=True, on_delete=models.SET_NULL)

    # Fields that provide information about what was sent in the body of the email
    emailto = models.EmailField() # to address of email # SHOULD THIS BE AN ARRAY FIELD TOO? PROBABLY
    emailcc = ArrayField(models.EmailField(), blank=True) # cc address(es) of email
    emailbcc = ArrayField(models.EmailField(), blank=True) # bcc address(es) of email
    subject = models.TextField(blank=True, default='') 
    body = models.TextField(blank=True, default='') 


    # "Meta" type fields 
    salutation = models.TextField(blank=True, default='')
    introduction = models.TextField(blank=True, default='')
    valueproposition = models.TextField(blank=True, default='')
    calltoaction = models.TextField(blank=True, default='')
    signature = models.TextField(blank=True, default='')

    introductionwordcount = models.IntegerField(blank=True, null=True)
    valuepropositionwordcount = models.IntegerField(blank=True, null=True)
    calltoactionwordcount = models.IntegerField(blank=True, null=True)

    # Fields that hold open/reply information
    numberofopens = models.IntegerField(blank=False, default=0)
    isrepliedto = models.BooleanField(default=False, null=False)
    # replysentiment # We will want to grade the reply an email gets, positive and successful or please go away

    def __str__(self):
        return "Email to {}, subject: {}".format(str(self.emailto), str(self.subject)) # Update this to hold relevant values
        # return "EMAIL"
    
    # On save action that does a word count of the various email pieces for example
    def save(self, *args, **kwargs):
        # introductionwordcount = self.word_count(self.introduction)
        # valuepropositionwordcount = self.word_count(self.valueproposition)
        # calltoactionwordcount = self.word_count(self.calltoaction)
        super(TimeStampedModel, self).save(*args, **kwargs)

    def word_count(self, string):
        word_list = string.split(" ")
        while '-' in word_list:
            word_list.remove('-')
        return len(word_list)

    class Meta:
        verbose_name = "email"
        verbose_name_plural = "emails"
        ordering = ('created',)
