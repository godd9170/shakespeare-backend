#import research.tests.constants as constants
from research.tests.constants.utilities import _mock_response
from django.contrib.auth.models import User
from django.urls import reverse
from research.models import Company, Individual, Research, Piece, Nugget
from rest_framework.test import APITestCase
from research.aggregators.storyzy import Storyzy
from requests.exceptions import HTTPError
# from research.aggregators.storyzy import Storyzy
# Standard library imports...
from unittest.mock import Mock, patch
import json, uuid


class FeaturedCustomersTests(APITestCase):

    def setUp(self):
        self._mock_response = _mock_response
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        # Create Individual
        self.individual = Individual(
                email='hgoddard@saasli.com', 
                clearbit=uuid.uuid4(), 
                companyname='ACME',
                firstname='Henry',
                lastname='Goddard')
        self.individual.save() #create individual
        # Create Research
        self.research = Research(individual=self.individual, owner=self.user)
        self.research.save() #create research


    @patch('research.aggregators.featuredcustomers.requests.get') #Fake the storyzy call
    def test_featuredcustomers_response_good(self, mock_featuredcustomers_request):
        mock_featuredcustomers_request.return_value = self._mock_response(self, json_data=constants.STORYZY_RESPONSE_GOOD)
        #mock_storyzy_request.return_value.json.return_value = constants.STORYZY_RESPONSE_GOOD
        #Execute the storyzy call
        FeaturedCustomers(research=self.research).execute()
        
        self.assertEqual(Piece.objects.count(), 2) #Check that 2 pieces were made
        self.assertEqual(Nugget.objects.count(), 2) #Check that 2 nuggets were made

    @patch('research.aggregators.featuredcustomers.requests.get') #Fake the storyzy call
    def test_featuredcustomers_response_bad(self, mock_featuredcustomers_request):
        mock_featuredcustomers_request.return_value = self._mock_response(self, status=500, raise_for_status=HTTPError("featuredcustomers is down"))
        #mock_storyzy_request.return_value.json.return_value = constants.STORYZY_RESPONSE_GOOD
        #Execute the storyzy call
        #self.assertRaises(HTTPError, Storyzy(research=self.research).execute)
        self.assertEqual(Piece.objects.count(), 0) #Check that 2 pieces were made
        self.assertEqual(Nugget.objects.count(), 0) #Check that 2 nuggets were made