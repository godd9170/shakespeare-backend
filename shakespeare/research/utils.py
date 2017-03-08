import json
import uuid
import clearbit
from research.models import Individual, Company
from research.exceptions import ContactNotFoundException
from django.core.exceptions import ObjectDoesNotExist

clearbit.key = 'sk_886efa2d89a51d9fc048d5d04023d09a' #TODO: Store this in settings


# Returns a new Individual Model, will attempt to associate an existing Company or make
# a new one should Clearbit have one.
def whois(email):
    #Fetch the person/company
    response = clearbit.Enrichment.find(email=email, stream=True) #get the clearbit person/company
    
    ## Individual
    person = response['person'] #clearbit
    individual = {'email' : email} #shakespeare
    if person is None: #if Clearbit can't find anyone, raise an exception
        raise ContactNotFoundException
    # Try to get individual info
    try:
        print('person {}'.format(person))
        name = person['name']
        employment = person['employment']
        individual.update({
            'lastname' : name['familyName'],
            'firstname' : name['givenName'],
            'avatar' : person['avatar'],
            'jobtitle' : employment['title'],
            'role' : employment['role'],
            'companyname' : employment['name'],
            'clearbit' : uuid.UUID(person['id'])
        })
    except Exception as e:
        print('Error in person response for {}: {}'.format(email, e))
        raise ContactNotFoundException

    ## Company
    company = response['company'] #clearbit
    organization = {} #shakespeare -> I'm calling the placeholder for what we return `organization`. Yes I realize this is confusing. Sue me.
    if (company is None) or (company.get('domain', None) is None): #if Clearbit can't find an org, or it doesn't have a domain don't bother associating an organization
        newIndividual = Individual(**individual)
        newIndividual.save()
        return newIndividual #Create the new individual without a company
    
    try: # See if we've got this company already
        newCompany = Company.objects.get(domain=company['domain']) 
    except ObjectDoesNotExist: # We don't have this company, let's see what Clearbit got, and we'll make a new one.
        # Try to get company info
        try:
            category = company['category']
            crunchbase = company['crunchbase']
            organization.update({
                'domain' : company['domain'],
                'name' : company['name'],
                'description' : company['description'],
                'industry' : category['industry'],
                'sector' : category['sector'],
                'crunchbase' : crunchbase['handle'],
                'logo' : company['logo'],
                'location' : company['geo'],
                'clearbit' : uuid.UUID(company['id'])
            })
            print("********************>>>>>>>>>>>>>>ORG!!!!!!!!!! {}".format(organization))
            newCompany = Company(**organization)
            newCompany.save()
            print("********************>>>>>>>>>>>>>>NEW COMPANY!!!!!!! {}".format(newCompany))
        except Exception as e:
            newIndividual = Individual(**individual)
            newIndividual.save()
            return newIndividual # We can't make a new org so just return an individual unassociated

    newIndividual = Individual(company=newCompany, **individual)
    newIndividual.save()
    return newIndividual #If we're here, we have a company model (either already existing or newly created)