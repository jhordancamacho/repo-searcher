from django.test import TestCase
from unittest.mock import MagicMock

from apps.github_search.domain.use_cases.search_use_case import SearchUseCase
from apps.github_search.data.repositories.repository import GithubRepository

class SearchUseCaseTest(TestCase):
    def test_execute_calls_repository_search(self):
        mock_repository = MagicMock()
        search_use_case = SearchUseCase(repository=mock_repository)
        query = "test_query"
        search_use_case.execute(query)
        mock_repository.search.assert_called_once_with(query)

class GithubRepositoryTest(TestCase):
    def test_search_constructs_correct_path_and_calls_api_get(self):
        mock_api = MagicMock()
        github_repository = GithubRepository(api=mock_api)
        query = "test_query"
        github_repository.search(query)
        expected_path = f"/search/repositories?q={query}"
        mock_api.get.assert_called_once_with(expected_path)
