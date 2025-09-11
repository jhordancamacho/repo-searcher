from ...api.api import Api

class GithubRepository:
    def __init__(self, api: Api):
        self.api = api

    def search(self, query: str):
        path = f"/search/repositories?q={query}"
        return self.api.get(path)
