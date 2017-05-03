import requests, json, re
from django.conf import settings
from research.models import Research, Piece, Nugget
from .aggregator import AbstractAggregator

RESOURCE_DOMAIN = 'https://predictleads.com/api/v1'

class PredictLeads(AbstractAggregator):
    
    def __init__(self, research):
        self.headers = {
            'X-User-Token': settings.PREDICT_LEADS_X_USER_TOKEN, # Include in Django settings
            'X-User-Email': settings.PREDICT_LEADS_X_USER_EMAIL # Include in Django settings
        }
        super().__init__(research)

    def request(self, signal_type):
        prospectDomain = self.research.individual.company.domain
        url = '{}/companies/{}/{}'.format(RESOURCE_DOMAIN, prospectDomain, signal_type)
        response = requests.get(url, headers=self.headers).json()
        setattr(self, signal_type, response['data'])


    # PredictLeads often throws a date on the end of the title, this function removes it
    def remove_date_from_pl_title(self, title):
        title = re.sub(r'\son\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(\s\d{1,2}(th?|st?|nd?))?(\s\d{2}\')?', '', title)
        return title


    # PredictLeads doesn't format dollar amounts well, this function inserts commas for each thousand
    # NEEDS TO BE UPDATED TO CONSIDER CURRENCY: PREDICT LEADS CURRENTLY DOES NOT RETURN THIS INFO HOWEVER
    def reformat_amount(self, amount_string):
        int_dollars = int(amount_string) # Cast to integer
        new_amount =  '$'+'{0:,}'.format(int_dollars) # Reformat and return
        return new_amount


    def execute(self, signal_type):
        if self.research.individual.company is not None:
            if (signal_type == "events"):
                self.do_predictleads_events()
            if (signal_type == "job_openings"):
                self.do_predictleads_jobopenings()

    def do_predictleads_events(self):
        self.request('events')
        for datum in self.events:
            attributes = datum.get('attributes')
            if attributes is not None:
                # If category exists in our own list create the piece, otherwise don't
                if self.category_exists(attributes['categories'][0]):
                    self.create_piece({
                        'aggregator' : 'PredictLeads',
                        'title' : self.reformat_article_title(self.remove_date_from_pl_title(attributes.get('title'))),
                        'url' : attributes.get('url'),
                        'publisheddate' : attributes.get('found_at'),
                        'group': self.category_to_group(attributes['categories'][0]),
                        'source' : {
                            'uri' : attributes.get('url'),
                            'domain' : self.parse_domain(attributes.get('url'))
                        }
                    })
                    additionaldata = attributes.get('additional_data')
                    if additionaldata is not None:
                        additionaldata['title'] = self.remove_date_from_pl_title(attributes.get('title'))
                        try:
                            additionaldata['amount'] = self.reformat_amount(additionaldata['amount'])
                        except:
                            pass
                        try:
                            self.create_nugget({
                                'additionaldata' : additionaldata,
                                'category' : attributes['categories'][0]
                            })
                        except:
                            print("No Category, no nugget")



    def do_predictleads_jobopenings(self):
        self.request('job_openings')
        if (len(self.job_openings) > 0): # Only create research if there are job openings
	        self.create_piece({
	            'aggregator' : 'PredictLeads',
	            'title' : 'Job Openings',
	            'author' : self.research.individual.company.name,
	            'publisheddate' : self.job_openings[0]['attributes']['found_at'],
	            'group': 'job_position' #can only every be job position
	        })
        for datum in self.job_openings:
            attributes = datum.get('attributes')
            additionaldata = attributes.get('additional_data')
            try:
                self.create_nugget({
                    'body' : attributes.get('title'),
                    'additionaldata' : additionaldata,
                    'category' : attributes['categories'][0]
                })
            except:
                print("No Category, no nugget")
