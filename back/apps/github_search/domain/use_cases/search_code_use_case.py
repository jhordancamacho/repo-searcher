from ...data.repositories.repository import GithubRepository


class SearchCodeUseCase:
    def __init__(self, repository: GithubRepository):
        self.repository = repository

    def execute(self, query: str):
        return self.repository.search_code(query)
