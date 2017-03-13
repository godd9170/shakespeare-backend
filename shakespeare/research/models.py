from django.db import models
from django.contrib.postgres.fields import JSONField # JSON Field
import uuid


class Company(models.Model):
    domain = models.CharField(unique=True, max_length=100) # Ensure the domain is unique
    created = models.DateTimeField(auto_now_add=True)
    clearbit = models.UUIDField() # The clearbit UUID
    name = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)
    crunchbase = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    logo = models.CharField(max_length=500, blank=True, null=True)
    location = JSONField() #json representation of location

    def __str__(self):
        return "{} ({})".format(str(self.name), str(self.domain))

    class Meta:
        verbose_name = "company"
        verbose_name_plural = "companies"
        ordering = ('created',)


# The individual to which research can be performed on. 
class Individual(models.Model):
    email = models.EmailField(unique=True) # Ensure that this email is unique
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    firstname = models.CharField(max_length=100, blank=True, null=True)
    lastname = models.CharField(max_length=100, blank=True, null=True)
    jobtitle = models.CharField(max_length=200, blank=True, null=True)
    role = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.CharField(max_length=500, blank=True, null=True) #URL to an avatar
    company = models.ForeignKey('research.Company', related_name='individual', null=True, on_delete=models.CASCADE) #null=True is because and Individual doesn't have to have a company
    companyname = models.CharField(max_length=200, blank=True, null=True) #We have a company name too, as it's possible for there to be no `company` result from Clearbit, however the person has a 'company name'
    clearbit = models.UUIDField() # The clearbit UUID

    def __str__(self):
        return "{} {} ({})".format(str(self.firstname),str(self.lastname), str(self.email))

    class Meta:
        verbose_name = "individual"
        verbose_name_plural = "individuals"
        ordering = ('created',)

# The specific research 'job' 
class Research(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #We'll use a UUID here to help anonymize the location of the results. 
    owner = models.ForeignKey('auth.User', related_name='research', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    individual = models.ForeignKey('research.Individual', related_name='research', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "research"
        verbose_name_plural = "research"
        ordering = ('created',)

# One 'result' of a search for information for the prospect.
class Piece(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    publisheddate = models.DateTimeField(null=True)
    title = models.TextField(blank=True, default='')
    author = models.CharField(max_length=1000, blank=True, default='')
    body = models.CharField(max_length=1000, blank=True, default='')
    source = models.CharField(max_length=1000, blank=True, default='') # We'll make this a text field for now. Ideally it's a lookup to a 'Data Source' table in the future
    url = models.TextField(blank=True, default='')
    research = models.ForeignKey('research.Research', related_name='piece', on_delete=models.CASCADE) #Lookup the research instance that spawned this
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "piece"
        verbose_name_plural = "pieces"
        ordering = ('created',)

# An NLP extracted 'snippet' of quotable/interesting/relevant material found within the body of a 'Piece'
class Nugget(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    speaker = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, choices=(('quote', 'Quote'), ('tweet', 'Tweet'), ('joblisting', 'Job Listing')), default='quote')
    entity = models.CharField(max_length=1000, blank=True, default='') #The person/place/thing responsible for this nugget
    body = models.CharField(max_length=1000, blank=True, default='') #The body of text comprising the nugget
    piece = models.ForeignKey('research.Piece', related_name='nugget', on_delete=models.CASCADE) #Lookup the research instance that spawned this
    
    def __str__(self):
        return self.body

    class Meta:
        verbose_name = "nugget"
        verbose_name_plural = "nuggets"
        ordering = ('created',)
