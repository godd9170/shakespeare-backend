import requests, json, re

from django.conf import settings
from research.models import Research, Piece, Nugget


# TO DO: this lives both here and in storyzy, it will move into an aggregator utils at some stage
# This function strips of the period at the end of an article title if there is one
def reformat_article_title(title):
    try:
        if title.endswith('.') or title.endswith(',') or title.endswith(';'):
            title = title[:-1]
    except:
        pass
    return title


# PredictLeads often throws a date on the end of the title, this function removes it
def remove_date_from_pl_title(title):
    title = re.sub(r'\son\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May?|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(\s\d{1,2}(th?|st?|nd?))?(\s\d{2}\')?', '', title)
    return title


def do_predictleads_events(research):
	company = research.individual.company # Get the domain name of the company for this research

	if company is not None:
		headers = {
			'X-User-Token': settings.PREDICT_LEADS_X_USER_TOKEN, # Include in Django settings
			'X-User-Email': settings.PREDICT_LEADS_X_USER_EMAIL # Include in Django settings
		}
		url = 'https://predictleads.com/api/v1/companies/' + company.domain + '/events'
		response = requests.get(url, headers=headers).json()

		data = response['data']

		for datum in data:
			research_piece = {
				'aggregator' : 'predictleads',
				'title' : reformat_article_title(remove_date_from_pl_title(datum['attributes']['title'])),
			    # 'body' : '',
			    'url' : datum['attributes']['url'],
			    'publisheddate' : datum['attributes']['found_at']
			}
			newPiece = Piece(research=research, **research_piece)
			newPiece.save()
			additionaldata = datum['attributes']['additional_data']
			additionaldata['title'] = remove_date_from_pl_title(datum.get('attributes').get('title'))
			nugget = {
				'additionaldata' : additionaldata
			}
			try:
				nugget.update({
				'category' : datum['attributes']['categories'][0]
				})
			except:
				nugget.update({
				'category' : ''
				})
			Nugget(piece=newPiece, **nugget).save()



def do_predictleads_jobopenings(research):
	company = research.individual.company # Get the domain name of the company for this research

	if company is not None:
		headers = {
			'X-User-Token': settings.PREDICT_LEADS_X_USER_TOKEN, # Include in Django settings
			'X-User-Email': settings.PREDICT_LEADS_X_USER_EMAIL # Include in Django settings
		}
		url = 'https://predictleads.com/api/v1/companies/' + company.domain + '/job_openings'
		response = requests.get(url, headers=headers).json()

		research_piece = {
				'aggregator' : 'PredictLeads',
				'title' : 'Job Openings',
			    # 'body' : '',
			    # 'url' : '',
			    'author' : company.name
			    # 'source' : '',
			}
		newPiece = Piece(research=research, **research_piece)
		newPiece.save()

		data = response['data']

		for datum in data:
			nugget = {
				'speaker' : '',
				'body' : datum['attributes']['title'],
				'additionaldata' : datum['attributes']['additional_data']
				# 'entity'
			}
			try:
				nugget.update({
				'category' : datum['attributes']['categories'][0]
				})
			except:
				nugget.update({
				'category' : ''
				})
			Nugget(piece=newPiece, **nugget).save()
