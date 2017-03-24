from datetime import datetime
import requests, json, pytz, re
from requests import HTTPError
from research.models import Research, Piece, Nugget
from .aggregator import AbstractAggregator

RESOURCE_DOMAIN = 'http://www.storyzy.com'

class Storyzy(AbstractAggregator):

    def __init__(self, research):
        super().__init__(research)

    def request(self):
        url = "{}/searchData?q={}".format(RESOURCE_DOMAIN, self.research.individual.companyname) #get
        resp = requests.get(url)
        resp.raise_for_status()
        self.quotes = resp.json()['searchResponse']



    def execute(self):
        if self.research.individual.companyname is not None:
            try:
                self.request()
                self.reshape_payload()
                for piece in self.research_pieces:
                    piece.pop('source_id', None) # source_id is no longer necessary
                    nuggets = piece.pop('nuggets', None) # get the nugget array
                    self.create_piece(piece)
                    for nugget in nuggets:
                        self.create_nugget(nugget)
            except HTTPError as e:
                print('Storyzy is Down: {}'.format(e))

    # This function removes double quotes throughout the quote
    def remove_double_quotes(self, body): 
        try: # Defensive. Try to reformat the company name if it needs reformatting.
            body = body.replace('\"','')
        except:
            pass
        return body


    # This function removes html tags within the quote
    def remove_html_tags(self, body):
        try:
            p = re.compile(r'<.*?>')
        except:
            pass
        return p.sub('', body)

    # This function removes any stock ticker symbols from quotes
    def remove_stock_ticker(self, quote):
        quote = re.sub(r'\s\(?((?i)AMEX?|NYSE?|NASDAQ?|FTSE?|DOW?|TSX?|SSE?|SZSE?|OMX?|DAX?|ASX?):\s?\w+\)?', '', quote)
        return quote

    # Generate the following data structure
    # research_pieces = [ 
    #     {
    #         "source_id" : 123,
    #         "title" : "dsfads",
    #         "publisher" : "sdfadsfas",
    #         "url" : "222.222.222",
    #         "date" : 12312312312,
    #         "nuggets" : [
    #             {
    #                 "category" : "quote",
    #                 "body": "asfsdf",
    #                 "speaker" : "mike"
    #             } 
    #         ]
    #     }
    # ]
    def reshape_payload(self):
        self.abouts = self.quotes.get('quotesAbout') if (self.quotes.get('quotesAbout') is not None) else []
        self.froms = self.quotes.get('quotesFrom') if (self.quotes.get('quotesFrom') is not None) else []
        allquotes = self.abouts + self.froms
        self.research_pieces = []
        for quote in allquotes:
            this_source = quote['source']
            if (this_source is not None and this_source.get('uri', None) is not None) :
                this_source['domain'] = self.parse_domain(this_source['uri'])


            speaker = quote['speakers'][0] ###ASSUMING 1st speak is the only speaker
            if (speaker.get('name') == (self.research.individual.firstname + " " + self.research.individual.lastname)):
                category = "quote_from_individual"
            else:
                category = "quote_from_company"
            
            if (speaker.get('from') == self.research.individual.companyname):
                category = "quote_from_company"

            nugget = {
                'body' : self.remove_stock_ticker(self.remove_double_quotes(self.remove_html_tags(quote['quote']))),
                'category' : category,
                'additionaldata' : {
                    'name' : speaker.get('name'),
                    'company' : speaker.get('from'),
                    'type' : speaker.get('type'),
                    'publisher' : this_source.get('publisher')
                }
            }
            this_research_piece = list(filter(lambda x: x.get('source_id') == this_source['id'], self.research_pieces)) #filter out all the elements that don't have that source id
            if len(this_research_piece) == 0: #this source hasn't showed up yet, let's make a new piece
                self.research_pieces.append({
                    'source_id' : this_source['id'],
                    'title' : self.reformat_article_title(this_source['title']),
                    'url' : this_source['uri'],
                    'publisheddate' : datetime.utcfromtimestamp(int(quote['date']/1000)).replace(tzinfo=pytz.utc),
                    'nuggets' : [nugget],
                    'source' : this_source,
                    'aggregator' : 'storyzy',
                    'group' : 'article' #TODO: fit into a more descriptive category (NLP?)
                })
            else: #we've already created the piece, grab it
                this_research_piece[0]['nuggets'].append(nugget)
