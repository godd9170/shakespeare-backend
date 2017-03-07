from django.contrib.auth.models import User
from django.test import TestCase # Might be redundant
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from research.models import Research
# Standard library imports...
from unittest.mock import Mock, patch
import json

class ResearchTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.user) #auth as the new user

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

    @patch('research.utils.requests.get') #Fake the actual request
    def test_create_research(self, mock_get):
        """
        Ensure we can create a new account object.
        """
        fullContactResponse = {
            'contactInfo' : 
                {
                    'familyName' : 'Goddard',
                    'givenName' : 'Henry'
                },
            'organizations': [
                {   
                    'current': True,
                    'name': 'Saasli',
                    'title': 'Solution Architect'
                }
            ],
            'photos': [
                {
                    'isPrimary': True,
                    'url': 'https://photo.com/pic'
                }
            ]  
        }
        mock_resp = self._mock_response(json_data=fullContactResponse)
        mock_get.return_value = mock_resp

        #Set up Request
        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        response = self.client.post(url, data, format='json')

        newObject = Research.objects.get()
        #Check for it in the DB
        self.assertEqual(Research.objects.count(), 1)
        self.assertEqual(newObject.email, 'testemail@email.com')
        
        #Check for the proper response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'id': str(newObject.id)}),
        # self.assertEqual(response.data, {
        #     'id': str(newObject.id),
        #     'firstname': newObject.firstname,
        #     'lastname': newObject.lastname,
        #     'email': newObject.email,
        #     'avatar': newObject.avatar,
        #     'jobtitle': newObject.jobtitle,
        #     'created': newObject.created,
        #     'company': newObject.company,
        #     'pieces': []
        # })

        
