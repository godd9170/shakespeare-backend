import requests
import json
from research import models

api_key = "5fa92173a917916a" #Store this in settings
url = "https://api.fullcontact.com/v2/person.json" #This too

def whois(email):
    r = requests.get(url, params={
        'email' : email, 
        'apiKey' : api_key
    })
    response = json.loads(r.text)
    print(response['photos'])
    avatar = next((photo for photo in response['photos'] if photo["isPrimary"] == True))['url']
    job = next((organizations for organizations in response['organizations'] if organizations["current"] == True))
    out = {
        'email' : email,
        'lastname' : response['contactInfo']['familyName'],
        'firstname' : response['contactInfo']['givenName'],
        'avatar' : avatar,
        'jobtitle' : job['title'],
        'company' : job['name'],
        'other_data' : response
    }
    print("OUT: {}".format(out))
    return out

#print(whois(email="godd9170@mylaurier.ca"))