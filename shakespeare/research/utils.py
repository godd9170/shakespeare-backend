import uuid

import clearbit
from django.core.exceptions import ObjectDoesNotExist

from .models import Individual, Company
from .exceptions import ContactNotFoundException, UnexpectedClearbitPersonPayload, UnexpectedClearbitCompanyPayload
from .aggregators.storyzy import do_storyzy
from .aggregators.predictleads import do_predictleads_events, do_predictleads_jobopenings
from .aggregators.featuredcustomers import do_featuredcustomers


clearbit.key = 'sk_886efa2d89a51d9fc048d5d04023d09a'  # TODO: Store this in settings


def get_research_pieces(research):
    do_storyzy(research) # Fetch + Build Research Pieces + Nuggets from Storyzy
    do_predictleads_events(research) # Get events from Predict Leads and build research pieces
    do_predictleads_jobopenings(research) # Get job openings from PredictLeads and build research pieces and nuggets
    do_featuredcustomers(research) # Get reviews from Featured Customers and build research pieces and nuggets


################################################################################################################
# TO DO LIST:
# - Company domain none and error considerations?  


def get_clearbit_person(response, email):
    ## Individual
    person = response['person']  # clearbit DOES THIS NEED A TRY? OR DOES THIS PART OF THE PAYLOAD ALWAYS EXIST?
    individual = {'email': email}  # shakespeare
    if person is None:  # if Clearbit can't find anyone, raise an exception
        raise ContactNotFoundException
        # Try to get individual info
    try:
        name = person['name']
        employment = person['employment']
        individual.update({
            'lastname': name['familyName'],
            'firstname': name['givenName'],
            'avatar': person['avatar'],
            'jobtitle': employment['title'],
            'role': employment['role'],
            'companyname': employment['name'],
            'clearbit': uuid.UUID(person['id'])
        })
        return individual
    except Exception as e:
        # print('Error in person response for {}: {}'.format(email, e))
        raise UnexpectedClearbitPersonPayload


def get_clearbit_company(response):
    ## Company
    company = response['company']  # clearbit DOES THIS NEED A TRY? OR DOES THIS PART OF THE PAYLOAD ALWAYS EXIST?
    organization = {}  # shakespeare -> I'm calling the placeholder for what we return `organization`. Yes I realize this is confusing. Sue me.
    # if company is None: #if Clearbit can't find anyone, raise an exception
    if (company is None) or (company.get('domain', None) is None):
        return None
    # Try to get company info
    try:
        try:
            category = company['category']
            crunchbase = company['crunchbase']
            organization.update({
                'domain': company['domain'],
                'name': company['name'],
                'description': company['description'],
                'industry': category['industry'],
                'sector': category['sector'],
                'crunchbase': crunchbase['handle'],
                'logo': company['logo'],
                'location': company['geo'],
                'clearbit': uuid.UUID(company['id'])
            })
            return organization
        except Exception as e:
            raise UnexpectedClearbitCompanyPayload  # WILL THIS ERROR MAKE ITS WAY TO ROLLBAR?
    except:
        return None


# Updates an existing individual, and may also either update or create a company.
def update_individual(email):
    updatedIndividual = Individual.objects.get(email=email)  # Find the existing individual
    response = clearbit.Enrichment.find(email=email, stream=True)  # get the clearbit person/company from previous id

    individual = get_clearbit_person(response, email)
    individual.update({'id': updatedIndividual.id, 'created': updatedIndividual.created})

    if individual is None:
        return  # Clearbit no longer has this person. Abort rest of the function.

    organization = get_clearbit_company(response)
    company = response['company']

    # If no company was returned from Clearbit, then make sure this is reflected in the individual
    if organization is None:
        updatedIndividual = Individual(company=None, **individual)
        updatedIndividual.save()
        return updatedIndividual

    # If a company was returned, check to see if it already exists in the database. If it does, update it.
    try:
        # Find existing company in database
        updatedCompany = Company.objects.get(domain=company['domain'])
        organization.update({'id': updatedCompany.id, 'created': updatedCompany.created})
        # Update company
        updatedCompany = Company(**organization)
        # for (key, value) in organization.items():
        # setattr(updatedCompany, key, value)
        updatedCompany.save()
        # Update individual
        updatedIndividual = Individual(company=updatedCompany, **individual)
        # for (key, value) in individual.items():
        #     setattr(updatedIndividual, key, value)
        updatedIndividual.save()
    except ObjectDoesNotExist:
        # Create company
        newCompany = Company(**organization)
        newCompany.save()
        # Update individual
        updatedIndividual = Individual(company=newCompany, **individual)
        # for (key, value) in individual.items():
        # setattr(updatedIndividual, key, value)
        updatedIndividual.save()

    return updatedIndividual


# Creates a new individual, and may also either update or create a company.
def create_individual(email):
    response = clearbit.Enrichment.find(email=email, stream=True)  # get the clearbit person/company

    individual = get_clearbit_person(response, email)

    organization = get_clearbit_company(response)
    company = response['company']

    # If no company was returned from Clearbit, only create an individual.
    if organization is None:
        newIndividual = Individual(**individual)
        newIndividual.save()
        return newIndividual  # Create the new individual without a company

    # If a company was returned, check to see if it already exists in the database. If not, create a new company, then individual.
    try:
        # If company was found, it should be updated in the database.
        updatedCompany = Company.objects.get(domain=company['domain'])
        organization.update({'id': updatedCompany.id, 'created': updatedCompany.created})
        # Update company
        updatedCompany = Company(**organization)
        # for (key, value) in organization.items():
        # setattr(updatedCompany, key, value)
        updatedCompany.save()

        newIndividual = Individual(company=updatedCompany, **individual)
        newIndividual.save()
    except ObjectDoesNotExist:
        # Create company
        newCompany = Company(**organization)
        newCompany.save()
        # Create individual
        newIndividual = Individual(company=newCompany,
                                   **individual)  # Create individual, and connect to the company we just made.
        newIndividual.save()

    return newIndividual