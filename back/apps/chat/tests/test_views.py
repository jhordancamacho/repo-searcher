from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.auth.test_mixins import AuthenticatedTestCase

from rest_framework import status
from unittest.mock import patch, MagicMock
from django.conf import settings

User = get_user_model()

class ChatViewTest(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()

        self.url = reverse('chat')  # Assuming the name is 'chat' from urls.py


    def test_unauthorized(self):
        self.client.credentials()  # Remove credentials
        response = self.client.post(self.url, {'prompt': 'hello'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_prompt(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'El campo "prompt" es requerido')

    @patch('apps.chat.views.OpenAI')
    @patch('apps.chat.views.settings')
    def test_success_simple(self, mock_settings, MockOpenAI):
        # Setup mocks
        mock_settings.LLM_BINDING_API_KEY = 'test-key'
        mock_settings.LLM_BINDING_HOST = 'http://test-host'
        mock_settings.LLM_MODEL = 'test-model'
        
        mock_client = MockOpenAI.return_value
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(message=MagicMock(content='Hello there!', tool_calls=None))
        ]
        mock_client.chat.completions.create.return_value = mock_response

        # Execute request
        response = self.client.post(self.url, {'prompt': 'Hi'})

        # Verify response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'Hello there!')
        self.assertEqual(response.data['prompt'], 'Hi')

        # Verify OpenAI called correctly
        MockOpenAI.assert_called_with(
            api_key='test-key',
            base_url='http://test-host'
        )

    @patch('apps.chat.views.OpenAI')
    @patch('apps.chat.views.settings')
    def test_openai_error(self, mock_settings, MockOpenAI):
        mock_settings.LLM_BINDING_API_KEY = 'test-key'
        
        mock_client = MockOpenAI.return_value
        mock_client.chat.completions.create.side_effect = Exception('OpenAI Error')

        response = self.client.post(self.url, {'prompt': 'Hi'})

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'OpenAI Error')
