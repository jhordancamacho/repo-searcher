from ...api.api import Api


class GithubRepository:
    def __init__(self, api: Api):
        self.api = api

    def search(self, query: str, language: str = None):
        path = f"/search/repositories?q={query}"
        if language:
            path += f"&language={language}"
        return self.api.get(path)

    def search_code(self, query: str):
        path = f"/search/code?q={query}"
        return self.api.get(path)
