# --------------------------
# Shakespeare API Constants
# --------------------------

SHAKESPEARE_NO_PERSON_RESPONSE = {
  "detail": "Unable to find a contact by that email."
}

# --------------------
# Clearbit Test Data
# --------------------
CLEARBIT_RESPONSE_GOOD = {
	"company": {
        "id": "840d8107-327a-4fa5-930a-a0c39e883e96",
        "category": {
            "industry": "Software",
            "sector": "Technology"
        },
        "crunchbase": {
            "handle": "/saasli"
        },
        "description": "Generic company description",
        "domain": "saasli.com",
        "geo": {
            "city": "Toronto",
            "country": "Canada",
            "countryCode": "CA",
            "lat": "43.6518083",
            "lng": "-79.3992626",
            "postalCode": "M5T2E2",
            "state": "Ontario",
            "stateCode": "ON",
            "streetName": "Spadina",
            "streetNumber": "251",
            "subPremise": "Suite 201"
        },
        "logo": "http://domain.com/logo.png",
        "name": "Saasli"
    },
    "person": {
        "id": "173cc909-a42b-4294-a6ba-712c2ccf73db",
        "avatar": "http://domain.com/avatar.png",
        "email": "clocke@saasli.com",
        "employment": {
            "domain": "saasli.com",
            "name": "Saasli",
            "role": "founder",
            "title": "founder"
        },
        "name": {
            "familyName": "Locke",
            "givenName": "Charlie"
        }
    }
}
CLEARBIT_RESPONSE_NO_PERSON = {
    "company": {
        "id": "840d8107-327a-4fa5-930a-a0c39e883e96",
        "category": {
            "industry": "Software",
            "sector": "Technology"
        },
        "crunchbase": {
            "handle": "/saasli"
        },
        "description": "Generic company description",
        "domain": "saasli.com",
        "geo": {
            "city": "Toronto",
            "country": "Canada",
            "countryCode": "CA",
            "lat": "43.6518083",
            "lng": "-79.3992626",
            "postalCode": "M5T2E2",
            "state": "Ontario",
            "stateCode": "ON",
            "streetName": "Spadina",
            "streetNumber": "251",
            "subPremise": "Suite 201"
        },
        "logo": "http://domain.com/logo.png",
        "name": "Saasli"
    },
    "person": None
}
CLEARBIT_RESPONSE_NO_COMPANY = {
    "company": None,
    "person": {
        "id": "173cc909-a42b-4294-a6ba-712c2ccf73db",
        "avatar": "http://domain.com/avatar.png",
        "email": "clocke@saasli.com",
        "employment": {
            "domain": "saasli.com",
            "name": "Saasli",
            "role": "founder",
            "title": "founder"
        },
        "name": {
            "familyName": "Locke",
            "givenName": "Charlie"
        }
    }
}


# --------------------
# Storyzy Test Data
# --------------------
STORYZY_RESPONSE_RESULTS = { 
    "searchResponse": {
        "quotesFrom": [   
            {
                "date": 1481754480000,
                "id": "5851ee08c3a8f433fd63d331",
                "quote": "Some of the new funding from Lightspeed will go toward marketing, including MTA subway ads, which is a growing trend among NYC-based startups (such as Handy, Seamless, Casper, Oscar, and <strong>JustWorks</strong>)",
                "relevanceScore": 1.8792,
                "source": {
                    "id": 12422846,
                    "publisher": "techcrunch.com",
                    "title": "Zola wedding registry raises $25 million from Lightspeed Venture Partners",
                    "uri": "https://techcrunch.com/2016/12/14/confirmed-zola-wedding-registry-raises-25-million-from-lightspeed-venture-partners/?ncid=rss"
                },
                "speakers": [
                    {
                        "id": "2711770",
                        "name": "Shan-Lyn Ma",
                        "publisher": false,
                        "type": "person"
                    }
                ]
            },
            {
                "date": 1481533200000,
                "id": "584eca0dc3a8f460b7f46d03",
                "quote": "<strong>Justworks</strong> has a great reputation in the industry and executes its business with integrity, which is something I value strongly. My goal as CFO is to provide the in-depth data, strategic analysis, and streamlined processes needed to help <strong>Justworks</strong> improve and grow as a company and to continue being a trusted partner to its growing customer base.",
                "source": {
                    "id": 12316061,
                    "publisher": "marketwired.com",
                    "title": "Justworks Names Michael Greten as Chief Financial Officer and Mario Springer as Vice President & Corporate Counsel",
                    "uri": "http://www.marketwired.com/press-release/justworks-names-michael-greten-as-chief-financial-officer-mario-springer-as-vice-president-2182439.htm"
                },
                "speakers": [
                    {
                        "from": "Justworks",
                        "id": "2639896",
                        "name": "Michael Greten",
                        "publisher": false,
                        "type": "person"
                    }
                ]
            }
        ]
    }
}

STORYZY_RESPONSE_NO_RESULTS = {}

# ---
# Mock Requests Response
# ---

# Thanks https://gist.github.com/evansde77/45467f5a7af84d2a2d34f3fcb357449c
def _mock_response(
        self,
        status=200,
        json_data=None,
        raise_for_status=None):
    """
    since we typically test a bunch of different
    requests calls for a service, we are going to do
    a lot of mock responses, so its usually a good idea
    to have a helper function that builds these things
    """
    mock_resp = Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    # add json data if provided
    if json_data:
        mock_resp.json.return_value = json_data
    return mock_resp