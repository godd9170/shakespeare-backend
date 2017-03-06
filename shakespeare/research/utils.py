import requests
import json
from research import models
from research.exceptions import ContactNotFoundException

api_key = "5fa92173a917916a" #Store this in settings
url = "https://api.fullcontact.com/v2/person.json" #This too

def whois(email):
    who = {'email' : email}
    r = requests.get(url, params={
        'email' : email, 
        'apiKey' : api_key
    })

    if r.status_code != 200: #if Full Contact couldn't find anyone, raise an exception
        raise ContactNotFoundException

    response = json.loads(r.text)

    # Try to get name
    try:
        who['lastname'] = response['contactInfo'].get('familyName', '')
        who['firstname'] = response['contactInfo'].get('givenName', '')
    except Exception as e:
        print('Unable to find name for {}'.format(email))

    # Try to get avatar
    try:
        who['avatar'] = next((photo for photo in response['photos'] if photo["isPrimary"] == True))['url']
    except Exception as e:
        print('Unable to find avatar for {}'.format(email))

    # Try to get job details
    try:
        job = next((organizations for organizations in response['organizations'] if organizations["current"] == True))
        who['jobtitle'] = job.get('title', '')
        who['company'] = job.get('name', '')
    except Exception as e:
        print('Unable to find job details for {}'.format(email))

    # Assign rest of response to other_data
    who['other_data'] = response

    print("OUT: {}".format(who))
    return who