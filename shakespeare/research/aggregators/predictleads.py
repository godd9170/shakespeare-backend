import requests
import json

from django.conf import settings
from research.models import Research, Piece, Nugget

def do_predictleads_events(research):
	# try:
	company = research.individual.company # Get the domain name of the company for this research
	# except Exception as e:
	# 	raise DomainNotFound

	if company is not None:
		headers = {
			'X-User-Token': settings.PREDICT_LEADS_X_USER_TOKEN, # Include in Django settings
			'X-User-Email': settings.PREDICT_LEADS_X_USER_EMAIL # Include in Django settings
		}

		url = 'https://predictleads.com/api/v1/companies/' + company.domain + '/events'

		response = requests.get(url, headers=headers).json()

		data = response['data']

		research_pieces = []
		for datum in data:
			research_piece = {
				'aggregator' : 'PredictLeads',
				'title' : datum['attributes']['title'],
			    'body' : '',
			    'url' : datum['attributes']['url'],
			    'publisheddate' : datum['attributes']['found_at']
			    # 'author' = 
			    # 'source' = 
			}
			newPiece = Piece(research=research, **research_piece)
			newPiece.save()
