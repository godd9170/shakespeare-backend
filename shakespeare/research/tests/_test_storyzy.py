import research.tests.constants as constants
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from research.models import Company, Individual, Research
from research.aggregators.storyzy import Storyzy
# Standard library imports...
from unittest.mock import Mock, patch
import json, uuid


class StoryzyTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.user) #auth as the new user


    @patch('research.utils.clearbit.Enrichment.find') #Fake the clearbit call
    def test_create_research_new_individual(self, mock_get):
        #mock_resp = self._mock_response(json_data=constants.CLEARBIT_RESPONSE)
        mock_get.return_value = constants.CLEARBIT_RESPONSE_GOOD

        #Set up Request
        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        response = self.client.post(url, data, format='json')
        newObject = Research.objects.get()
        
        self.assertEqual(Research.objects.count(), 1) #Check for a new research piece
        self.assertEqual(Individual.objects.count(), 1) #Check for a new Individual
        self.assertEqual(Company.objects.count(), 1) #Check for a new Company
        
        self.assertEqual(response.data, {'id': str(newObject.id)}) #Check for the proper response