from datetime import datetime
import requests, json, pytz, re
from research.models import Research, Piece, Nugget

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
def remove_double_quotes(body): # This function removes double quotes throughout the quote
    try: # Defensive. Try to reformat the company name if it needs reformatting.
        body = body.replace('\"','')
    except:
        pass
    return body

def remove_html_tags(body): # This function removes html tags within the quote
    p = re.compile(r'<.*?>')
    return p.sub('', body)


def reshape_payload(quotes, category, individual=None):
    research_pieces = []
    for quote in quotes:
        this_source = quote['source']
        speaker = quote['speakers'][0] ###ASSUMING 1st speak is the only speaker
        if (category == "quote_from"):
            if (speaker.get('name') == (individual.firstname + " " + individual.lastname)):
                category = "quote_from_individual"
            else:
                category = "quote_from_company"
        nugget = {
            'body' : remove_double_quotes(remove_html_tags(quote['quote'])),
            'category' : category,
            'additionaldata' : {
                'name' : speaker.get('name'),
                'company' : speaker.get('from'),
                'type' : speaker.get('type'),
                'publisher' : this_source.get('publisher')
            }
        }
        this_research_piece = list(filter(lambda x: x.get('source_id') == this_source['id'], research_pieces)) #filter out all the elements that don't have that source id
        if len(this_research_piece) == 0: #this source hasn't showed up yet, let's make a new piece
            research_pieces.append({
                'source_id' : this_source['id'],
                'title' : this_source['title'],
                'url' : this_source['uri'],
                'publisheddate' : datetime.utcfromtimestamp(int(quote['date']/1000)).replace(tzinfo=pytz.utc),
                'nuggets' : [nugget],
                'source' : this_source,
                'aggregator' : 'storyzy'
            })
        else: #we've already created the piece, grab it
            this_research_piece[0]['nuggets'].append(nugget)
    return research_pieces

def do_storyzy(research):
    companyName = research.individual.companyname #get the name of the company for this research
    if companyName is not None:
        url = "http://www.storyzy.com/searchData?q={}".format(companyName) #get 
        response = requests.get(url).json()
        # obtain an array of quotes
        research_pieces = reshape_payload(response['searchResponse']['quotesAbout'], 'quote_about') + reshape_payload(response['searchResponse']['quotesFrom'], 'quote_from', research.individual)
        for piece in research_pieces:
            piece.pop('source_id', None) # source_id is no longer necessary
            nuggets = piece.pop('nuggets', None) # get the nugget array
            newPiece = Piece(research=research, **piece)
            newPiece.save() #.full_clean()
            for nugget in nuggets:
                Nugget(piece=newPiece, **nugget).save() #.full_clean()

    


#print(json.dumps(story(companyName), indent=4, sort_keys=True))
