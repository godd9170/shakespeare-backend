from unittest import mock

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from research.models import Research
from research.tests.constants import CLEARBIT_RESPONSE_GOOD


class ResearchTasksTests(APITestCase):
    def setUp(self):
        """
        1) Authenticate an user
        """
        self.user = User.objects.create_user('john', 'john@snow.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.client.force_authenticate(user=self.user)

    @mock.patch('research.views.get_research_pieces_task.delay')
    @mock.patch('research.utils.clearbit.Enrichment.find')
    def test_task_called(self, mock_find, mock_get_research_pieces_task):
        mock_find.return_value = CLEARBIT_RESPONSE_GOOD

        # Check that we have no research in the database whatsoever
        self.assertEqual(len(Research.objects.all()), 0)

        url = reverse('create_research')
        data = {'email': 'testemail@email.com'}

        # Hit the endpoint to trigger the creation of a research object
        self.client.post(url, data, format='json')

        research_objects = Research.objects.all()
        self.assertEqual(len(research_objects), 1)

        research = research_objects[0]

        mock_get_research_pieces_task.assert_called_once_with(research_id=research.id)



