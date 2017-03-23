import requests
import json
from bs4 import BeautifulSoup
from django.conf import settings
from research.models import Research, Piece, Nugget

RESOURCE_DOMAIN = 'https://www.featuredcustomers.com'

class FeaturedCustomers(object):

    def __init__(self, research):
        self.research = research
        self.companyName = self.research.individual.companyname

    def execute(self):
        self.format_company_name() # Normalize the company name
        self.get_testimonials_page_content() # Retrieve the testimonials page
        self.parse_testimonials() # Scrape the testimonials from the html

    def get_testimonials_page_content(self):
        """
        Request the html page likely containing the customer testimonials
        """
        url = '{}/vendor/{}/testimonials'.format(RESOURCE_DOMAIN, self.companyName)
        self.content = requests.get(url).content

    def format_company_name(self):
        """
        Used to format spaces and 'inc's out of the company name as these do not appear in the FeaturedCustomers URLs
        """
        try: # Defensive. Try to reformat the company name if it needs reformatting.
            if self.companyName.endswith(', Inc.') or self.companyName.endswith(', inc.'):
                self.companyName = self.companyName[:-6]
            elif self.companyName.endswith(' Inc.') or self.companyName.endswith(' inc.'):
                self.companyName = self.companyName[:-5]
            elif self.companyName.endswith(', Inc') or self.companyName.endswith(', inc'):
                self.companyName = self.companyName[:-5]
            elif self.companyName.endswith(' Inc') or self.companyName.endswith(' inc'):
                self.companyName = self.companyName[:-4]
            
            self.companyName = self.companyName.replace(' ', '')
        except:
            print('Could not convert company name with available methods.')

    def parse_testimonials(self):
        """
        BeautifulSoup the html markup into something a little more usable
        """
        soup = BeautifulSoup(self.content, "html.parser")#, 'html.parser')
        review_block = soup.find_all('div', {'class' : 'review_companies'})
        if self.companyName is not None:
            if len(review_block) > 0: # Only create research if we find reviews for this company
                research_piece = {
                    'aggregator' : 'FeaturedCustomers',
                    'title' : 'Customer Testimonials',
                    'author' : 'Misc. Authors'
                }
                newPiece = Piece(research=self.research, **research_piece)
                newPiece.save()

                for item in review_block:
                    # print(item.find_all('span', {'class' : 'subtitle'})[0].text)
                    reviewerFullName = item.find_all('h2', {'itemprop' : 'name'})[0].text
                    reviewerCompanyName = item.find_all('span', {'class' : 'subtitle'})[0].text
                    reviewerTitle = item.find_all('a')[0].get('title')
                    testimonial = item.find_all('div', {'itemprop' : 'reviewBody'})[0].text
                    nugget = {
                        'body' : testimonial,
                        'category' : 'testimonial',
                        'additionaldata' : { 
                            'name' : reviewerFullName, 
                            'company' : reviewerCompanyName,
                            'title' : reviewerTitle 
                        }
                    }
                    Nugget(piece=newPiece, **nugget).save()