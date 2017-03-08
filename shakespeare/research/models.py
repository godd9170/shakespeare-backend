from django.db import models
from django.contrib.postgres.fields import JSONField # JSON Field
import uuid

class Individual(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    firstname = models.CharField(max_length=100, blank=True, default='')
    lastname = models.CharField(max_length=100, blank=True, default='')
    jobtitle = models.CharField(max_length=100, blank=True, default='')
    avatar = models.CharField(max_length=500, blank=True, default='') #URL to an avatar
    company = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return "{} {} ({})".format(str(self.firstname),str(self.lastname), str(self.email))

    class Meta:
        verbose_name = "research"
        verbose_name_plural = "research"
        ordering = ('created',)

# The specific research 'job' 
class Research(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #We'll use a UUID here to help anonymize the location of the results. 
    owner = models.ForeignKey('auth.User', related_name='research', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    other_data = JSONField() #All the fullcontact (or w/e we use) results
    individual = models.ForeignKey('research.Individual', related_name='research', on_delete=models.CASCADE) #Lookup the individual for which this research is for.

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "research"
        verbose_name_plural = "research"
        ordering = ('created',)

# One 'result' of a search for information for the prospect.
class Piece(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    author = models.CharField(max_length=1000, blank=True, default='')
    body = models.CharField(max_length=1000, blank=True, default='')
    source = models.CharField(max_length=1000, blank=True, default='') # We'll make this a text field for now. Ideally it's a lookup to a 'Data Source' table in the future
    research = models.ForeignKey('research.Research', related_name='piece', on_delete=models.CASCADE) #Lookup the research instance that spawned this
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "research piece"
        verbose_name_plural = "research pieces"
        ordering = ('created',)

# An NLP extracted 'snippet' of quotable/interesting/relevant material found within the body of a 'Piece'
class Nugget(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    actor = models.CharField(max_length=1000, blank=True, default='') #The person/place/thing responsible for this nugget
    body = models.CharField(max_length=1000, blank=True, default='') #The body of text comprising the nugget
    #class = models. #We'll need some form of classifier here, that tells us if this is a quote, tweet, video, paraphrase etc. etc.
    piece = models.ForeignKey('research.Piece', related_name='nugget', on_delete=models.CASCADE) #Lookup the research instance that spawned this
    
    def __str__(self):
        return self.body

    class Meta:
        verbose_name = "nugget"
        verbose_name_plural = "nuggets"
        ordering = ('created',)
