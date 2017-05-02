import uuid
import re
import clearbit
from django.core.exceptions import ObjectDoesNotExist

from .models import Individual, Company
from .exceptions import ContactNotFoundException, UnexpectedClearbitPersonPayload, UnexpectedClearbitCompanyPayload


################################################################################################################
# TO DO LIST:
# - Company domain none and error considerations?  

# This function makes sure that job titles are appropriately capitalised for presentation in browser. Clearbit has proved not great in this regard.
def reformat_job_title(title):
    if title is not None:
        original_words = title.split(" ")
        updated_words =[]
        stop_words = ['of', 'and']

        for word in original_words:
            if word not in stop_words:
                word = word.capitalize()
            updated_words.append(word)

        return ' '.join(updated_words)
    return title


def clean_company_name(company_name):
    if company_name is not None:
        company_name = re.sub(r'(?i)\,?\s+(?:corp(?:oration)?|inc(?:orporated)?|(gmbh)|(llc)|(ltd)|(lllp))\.?', '', company_name)
    return company_name


def get_clearbit_person(response, email):
    ## Individual
    try:
        person = response['person']
        individual = {'email': email}
    except:
        raise ContactNotFoundException
    # Try to get individual info
    if person['avatar'] is None: # If we can't find a picture for the individual, show the company logo
        try: # ...assuming that a company payload exists that is
            avatar = response['company']['logo']
        except:
            avatar = 'https://s3.amazonaws.com/shakespeare-images/default_avatar.png'
    else:
        avatar = person['avatar']

    try:
        name = person['name']
        employment = person['employment']
        individual.update({
            'lastname': name['familyName'],
            'firstname': name['givenName'],
            'avatar': avatar,
            'jobtitle': reformat_job_title(employment['title']),
            'role': employment['role'],
            'companyname': employment['name'],
            'clearbit': uuid.UUID(person['id']),
            'linkedinhandle': person['linkedin']['handle']
        })
        return individual
    except Exception as e:
        print('Error in person response for {}: {}'.format(email, e))
        # raise UnexpectedClearbitPersonPayload


def get_clearbit_company(response):
    ## Company
    try:
        company = response['company']  # clearbit DOES THIS NEED A TRY? OR DOES THIS PART OF THE PAYLOAD ALWAYS EXIST?
        organization = { 'domain' : company['domain'] }  # shakespeare -> I'm calling the placeholder for what we return `organization`. Yes I realize this is confusing. Sue me.
    except:
        raise ContactNotFoundException # TO DO: HANDLE COMPANY NOT FOUND APPROPRIATELY

    # Try to get company info
    try:
        try:
            category = company['category']
            crunchbase = company['crunchbase']
            organization.update({
                'domain': company['domain'],
                'name': company['name'],
                'cleanedname': clean_company_name(company['name']),
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

    try:
        individual = get_clearbit_person(response, email)
        individual.update({'id': updatedIndividual.id, 'created': updatedIndividual.created})
    except:
        return updatedIndividual

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
    try:
        response = dict(clearbit.Enrichment.find(email=email, stream=True))  # get the clearbit person/company
    except:
        raise ContactNotFoundException

    if (response is not None and response.get('person')):
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
            newIndividual = Individual(company=newCompany, **individual)  # Create individual, and connect to the company we just made.
            newIndividual.save()

        return newIndividual
    else:
        raise ContactNotFoundException


# Create an individual from individual and company data objects manually entered on the frontend
def create_indiviual_without_clearbit(individualObject, companyObject):
    try:
        company = Company.objects.get(domain=companyObject['companydomain'])
    except:
        organization = {
            'domain': companyObject['companydomain'],
            'name': companyObject['companyname'],
            'cleanedname': clean_company_name(companyObject['companyname'])
        }
        company = Company(**organization)
        company.save()

    individual = {
        'email' : individualObject['email'],
        'firstname' : individualObject['firstname'],
        'lastname' : individualObject['lastname'],
        'jobtitle' : individualObject['jobtitle'],
        'companyname' : companyObject['companyname']
    }
    newIndividual = Individual(company=company, **individual)
    newIndividual.save()
    return newIndividual
