from django.test import TestCase
from unittest.mock import patch, MagicMock
import requests
from django.conf import settings

from apps.github_search.api.api import Api

class ApiTest(TestCase):
    def setUp(self):
        # Set a dummy GITHUB_TOKEN for testing
        self.original_github_token = getattr(settings, 'GITHUB_TOKEN', None)
        settings.GITHUB_TOKEN = "test_token"
        self.api = Api()

    def tearDown(self):
        # Restore original GITHUB_TOKEN
        if self.original_github_token is not None:
            settings.GITHUB_TOKEN = self.original_github_token
        elif hasattr(settings, 'GITHUB_TOKEN'):
            del settings.GITHUB_TOKEN

    @patch('requests.get')
    def test_get_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"key": "value"}
        mock_requests_get.return_value = mock_response

        path = "/test"
        result = self.api.get(path)

        mock_requests_get.assert_called_once_with(f"{self.api.base_url}{path}", headers={"Authorization": f"token {settings.GITHUB_TOKEN}"})
        self.assertEqual(result, {"key": "value"})
        mock_response.raise_for_status.assert_called_once()

    @patch('requests.get')
    def test_get_http_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_response)
        mock_requests_get.return_value = mock_response

        path = "/test"
        with self.assertRaises(requests.exceptions.HTTPError):
            self.api.get(path)

        mock_requests_get.assert_called_once_with(f"{self.api.base_url}{path}", headers={"Authorization": f"token {settings.GITHUB_TOKEN}"})
        mock_response.raise_for_status.assert_called_once()

    @patch('requests.get')
    def test_get_authorization_header(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_requests_get.return_value = mock_response

        path = "/test"
        self.api.get(path)

        expected_headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
        mock_requests_get.assert_called_once()
        # Check that the headers passed to requests.get match our expectation
        self.assertIn('headers', mock_requests_get.call_args.kwargs)
        self.assertEqual(mock_requests_get.call_args.kwargs['headers'], expected_headers)
