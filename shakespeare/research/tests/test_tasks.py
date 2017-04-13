import uuid
from unittest.mock import Mock, patch

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
#from research.tasks import storyzy_task, predictleadsevents_task, predictleadsjobs_task, featuredcustomers_task

from research.models import Research, Individual
from research.tests.constants.clearbit import CLEARBIT_RESPONSE_GOOD


class ResearchTasksTests(APITestCase):
    def setUp(self):
        """
        1) Authenticate a user
        """
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.user)
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

    @patch('research.tasks.extract_article_bodies_task.s')
    @patch('research.tasks.featuredcustomers_task.s')
    @patch('research.tasks.predictleadsjobs_task.s')
    @patch('research.tasks.predictleadsevents_task.s')
    @patch('research.tasks.storyzy_task.s')
    @patch('research.tasks.chain')
    @patch('research.tasks.chord')
    @patch('research.utils.clearbit.Enrichment.find') # Patch clearbit so not to burn credits 
    def test_tasks_called(self, 
            mock_find, 
            mock_chord, 
            mock_chain,
            storyzy_task, 
            predictleadsevents_task, 
            predictleadsjobs_task, 
            featuredcustomers_task,
            extract_article_bodies_task):
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.user)
        url = reverse('create_research')
        data = {'email': 'hgoddard@saasli.com'}

        # Hit the endpoint to trigger the creation of a research object
        self.client.post(url, data, format='json')
        mock_chord.assert_called_once_with(
            [
                mock_chain(predictleadsevents_task(self.research.id), extract_article_bodies_task(self.research.id)),
                mock_chain(storyzy_task(self.research.id), extract_article_bodies_task(self.research.id)),
                predictleadsjobs_task(self.research.id), 
                featuredcustomers_task(self.research.id)
            ]
        )



