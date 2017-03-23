import research.tests.constants as constants
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from research.models import Company, Individual, Research
# Standard library imports...
from unittest.mock import Mock, patch
import json, uuid

class ResearchTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.user) #auth as the new user

    @patch('research.utils.clearbit.Enrichment.find') #Fake the clearbit call
    def test_create_research_new_individual(self, mock_find):
        #mock_resp = self._mock_response(json_data=constants.CLEARBIT_RESPONSE)
        mock_find.return_value = constants.CLEARBIT_RESPONSE_GOOD

        #Set up Request
        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        response = self.client.post(url, data, format='json')
        newObject = Research.objects.get()
        
        self.assertEqual(Research.objects.count(), 1) #Check for a new research piece
        self.assertEqual(Individual.objects.count(), 1) #Check for a new Individual
        self.assertEqual(Company.objects.count(), 1) #Check for a new Company
        
        self.assertEqual(response.data, {'id': str(newObject.id)}) #Check for the proper response
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

    @patch('research.utils.clearbit.Enrichment.find') #Fake the clearbit call
    def test_create_research_new_individual_no_person(self, mock_get):
        mock_get.return_value = constants.CLEARBIT_RESPONSE_NO_PERSON

        #Set up Request
        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        response = self.client.post(url, data, format='json')

        self.assertEqual(Research.objects.count(), 0) #Check for no new research piece
        self.assertEqual(Individual.objects.count(), 0) #Check no new Individual
        self.assertEqual(Company.objects.count(), 0) #Check no new Company
        
        self.assertEqual(response.data, constants.SHAKESPEARE_NO_PERSON_RESPONSE) #Check for the proper no person response

    @patch('research.utils.clearbit.Enrichment.find') #Fake the clearbit call
    def test_create_research_new_individual_no_company(self, mock_get):
        mock_get.return_value = constants.CLEARBIT_RESPONSE_NO_COMPANY

        #Set up Request
        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        response = self.client.post(url, data, format='json')

        newObject = Research.objects.get()

        self.assertEqual(Research.objects.count(), 1) #Check for a new research piece
        self.assertEqual(Individual.objects.count(), 1) #Check a new Individual
        self.assertEqual(Company.objects.count(), 0) #Check no new Company
        
        #Check for the proper response
        self.assertEqual(response.data, {'id': str(newObject.id)})

    @patch('research.utils.clearbit.Enrichment.find') #Fake the clearbit call
    def test_create_research_existing_individual(self, mock_get):
        mock_get.return_value = constants.CLEARBIT_RESPONSE_GOOD
        Individual(email='testemail@email.com', clearbit=uuid.uuid4()).save() # Create an already existing individual
        self.assertEqual(Individual.objects.count(), 1) #Check for it in the DB
        #Set up Request
        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        response = self.client.post(url, data, format='json')

        newObject = Research.objects.get()
        self.assertEqual(Research.objects.count(), 1) #Check that a research object was created
        self.assertEqual(Individual.objects.count(), 1) #Check that no new Individuals are created
        self.assertEqual(response.data, {'id': str(newObject.id)}) #Check for the proper response


        
