import requests
from django.conf import settings

class Api:
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.token = settings.GITHUB_TOKEN

    def get(self, path):
        headers = {
            "Authorization": f"token {self.token}"
        }
        response = requests.get(f"{self.base_url}{path}", headers=headers)
        response.raise_for_status()
        return response.json()
