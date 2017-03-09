import requests
import json
import datetime
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
def reshape_payload(quotes):
    research_pieces = []
    for quote in quotes:
        this_source = quote['source']
        nugget = {
            'body' : quote['quote'],
            'category' : 'quote',
            'speaker' : quote['speakers'][0]['name'] ###ASSUMING 1st speak is the only speaker
        }
        this_research_piece = list(filter(lambda x: x.get('source_id') == this_source['id'], research_pieces)) #filter out all the elements that don't have that source id
        if len(this_research_piece) == 0: #this source hasn't showed up yet, let's make a new piece
            research_pieces.append({
                'source_id' : this_source['id'],
                'title' : this_source['title'],
                'url' : this_source['uri'],
                'publisheddate' : datetime.datetime.fromtimestamp(int(quote['date']/1000)),
                'nuggets' : [nugget]
            })
        else: #we've already created the source, grab it
            this_research_piece[0]['nuggets'].append(nugget)
    return research_pieces

def do_storyzy(research):
    companyName = research.individual.companyname #get the name of the company for this research
    url = "http://www.storyzy.com/searchData?q={}".format(companyName) #get 
    response = requests.get(url).json()
    # obtain an array of quotes
    research_pieces = reshape_payload(response['searchResponse']['quotesAbout'])
    for piece in research_pieces:
        piece.pop('source_id', None) # source_id is no longer necessary
        nuggets = piece.pop('nuggets', None) # get the nugget array
        newPiece = Piece(research=research, **piece)
        newPiece.save()
        for nugget in nuggets:
            Nugget(piece=newPiece, **nugget).save() #Make the new nugget

    


#print(json.dumps(story(companyName), indent=4, sort_keys=True))