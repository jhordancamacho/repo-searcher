from ...data.repositories.repository import GithubRepository

class SearchUseCase:
    def __init__(self, repository: GithubRepository):
        self.repository = repository

    def execute(self, query: str):
        return self.repository.search(query)
