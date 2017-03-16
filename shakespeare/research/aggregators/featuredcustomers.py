import requests
import json
from bs4 import BeautifulSoup

from django.conf import settings
from research.models import Research, Piece, Nugget


# Used to format spaces and 'inc's out of the company name as these do not appear in the FeaturedCustomers URLs
def format_company_name(company):
    try: # Defensive. Try to reformat the company name if it needs reformatting.
        if company.endswith(', Inc.') or company.endswith(', inc.'):
            company = company[:-6]
        elif company.endswith(' Inc.') or company.endswith(' inc.'):
            company = company[:-5]
        elif company.endswith(', Inc') or company.endswith(', inc'):
            company = company[:-5]
        elif company.endswith(' Inc') or company.endswith(' inc'):
            company = company[:-4]
        
        company = company.replace(' ', '')
    except:
        print('Could not convert company name with available methods.')
    return company

def do_featuredcustomers(research):
    companyName = research.individual.companyname # Get the company of the individual
    if companyName is not None:
        formated_company = format_company_name(companyName)
        url = 'https://www.featuredcustomers.com/vendor/' + format_company_name(companyName) + '/testimonials'  
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")#, 'html.parser')
        review_block = soup.find_all('div', {'class' : 'review_companies'})

        if len(review_block) > 0: # Only create research if we find reviews for this company
            research_piece = {
                'aggregator' : 'FeaturedCustomers',
                'title' : 'Customer Testimonials',
                # 'body' : '',
                # 'url' : '',
                'author' : 'Misc. Authors'
                # 'source' : '',
            }
            newPiece = Piece(research=research, **research_piece)
            newPiece.save()

            for item in review_block:
                # print(item.find_all('span', {'class' : 'subtitle'})[0].text)
                reviewerFullName = item.find_all('h2', {'itemprop' : 'name'})[0].text
                reviewerCompanyName = item.find_all('span', {'class' : 'subtitle'})[0].text
                reviewerTitle = item.find_all('a')[0].get('title')
                testimonial = item.find_all('div', {'itemprop' : 'reviewBody'})[0].text
                nugget = {
                    'speaker' : reviewerFullName,
                    'body' : testimonial,
                    'category' : 'quote'
                    # 'entity'
                }
                Nugget(piece=newPiece, **nugget).save()
