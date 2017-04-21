from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class Persona(TimeStampedModel):
    title = models.CharField(max_length=100, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='personas', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "personas"
        ordering = ('created',)

class ValueProposition(TimeStampedModel):
    title = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='')
    # personas = models.ManyToManyField(Persona, related_name='value_proposition_personas') #related name is how Persona will refer to it's ValuePropositions
    active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='valueprops', on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "value proposition"
        verbose_name_plural = "value propositions"
        ordering = ('created',)


class CallToAction(TimeStampedModel):
    title = models.TextField(blank=True, default='')
    body = models.TextField(blank=True, default='')
    # personas = models.ManyToManyField(Persona, related_name='call_to_action_personas')
    active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='calltoactions', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "call to action"
        verbose_name_plural = "calls to action"
        ordering = ('created',)