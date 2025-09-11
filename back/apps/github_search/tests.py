from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock

class RepositorySearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('repository-search')

    def test_search_view_missing_query_param(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Query parameter "q" is required'})

    @patch('apps.github_search.views.Api')
    def test_search_view_success(self, MockApi):
        mock_api_instance = MockApi.return_value
        mock_api_instance.get.return_value = {
            'items': [
                {
                    'id': 1,
                    'name': 'test-repo',
                    'full_name': 'test/test-repo',
                    'owner': {
                        'id': 1,
                        'login': 'test',
                        'avatar_url': 'http://example.com/avatar',
                        'html_url': 'http://example.com/test'
                    },
                    'html_url': 'http://example.com/test/test-repo',
                    'description': 'A test repository',
                    'stargazers_count': 10,
                    'language': 'Python',
                    'forks_count': 5,
                    'open_issues_count': 2,
                    'created_at': '2023-01-01T12:00:00Z',
                    'updated_at': '2023-01-01T12:00:00Z'
                }
            ]
        }

        response = self.client.get(self.url, {'q': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['name'], 'test-repo')