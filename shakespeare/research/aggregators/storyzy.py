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
def remove_double_quotes(body):
    try: # Defensive. Try to reformat the company name if it needs reformatting.
        body = body.replace('\"','')
    except:
        pass
    return body

def remove_html_tags(body):
    p = re.compile(r'<.*?>')
    return p.sub('', body)


def reshape_payload(quotes, category):
    research_pieces = []
    for quote in quotes:
        print('>>>>>>>>>>>>>>>>QUOTE: {}'.format(quote))
        this_source = quote['source']
        speaker = quote['speakers'][0] ###ASSUMING 1st speak is the only speaker
        quote_body = remove_double_quotes(remove_html_tags(quote['quote']))
        nugget = {
            'body' : quote_body,
            'category' : category,
            'additionaldata' : {
                'name' : speaker.get('name'),
                'company' : speaker.get('from'),
                'type' : speaker.get('type'),
                'publisher' : speaker.get('publisher')
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
                'source' : this_source
            })
        else: #we've already created the piece, grab it
            this_research_piece[0]['nuggets'].append(nugget)
    return research_pieces

def do_storyzy(research):
    companyName = research.individual.companyname #get the name of the company for this research
    if companyName is not None:
        query = companyName + '%20' + research.individual.firstname + '%20' + research.individual.lastname 
        # url = "http://www.storyzy.com/searchData?q={}".format(companyName) #get 
        url = "http://www.storyzy.com/searchData?q={}".format(query)
        response = requests.get(url).json()
        # obtain an array of quotes
        research_pieces = reshape_payload(response['searchResponse']['quotesAbout'], 'quote_about') + reshape_payload(response['searchResponse']['quotesFrom'], 'quote_from')
        for piece in research_pieces:
            piece.pop('source_id', None) # source_id is no longer necessary
            nuggets = piece.pop('nuggets', None) # get the nugget array
            newPiece = Piece(research=research, **piece)
            newPiece.save() #.full_clean()
            for nugget in nuggets:
                Nugget(piece=newPiece, **nugget).save() #.full_clean()

    


#print(json.dumps(story(companyName), indent=4, sort_keys=True))
