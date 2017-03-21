import requests
import json

from django.conf import settings
from research.models import Research, Piece, Nugget

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
				'title' : datum['attributes']['title'],
			    # 'body' : '',
			    'url' : datum['attributes']['url'],
			    'publisheddate' : datum['attributes']['found_at']
			}
			newPiece = Piece(research=research, **research_piece)
			newPiece.save()
			nugget = {
				'additionaldata' : datum['attributes']['additional_data']
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
			additionaldata = datum['attributes']['additional_data']
			additionaldata['title'] = datum['attributes'].get('title')
			nugget = {
				'speaker' : '',
				'body' : datum['attributes']['title'],
				'additionaldata' : additionaldata
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
