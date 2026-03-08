from rest_framework.views import APIView
from rest_framework.response import Response
from .api.api import Api
from .data.repositories.repository import GithubRepository
from .domain.use_cases.search_use_case import SearchUseCase
from .domain.use_cases.search_code_use_case import SearchCodeUseCase
from .serializer import RepositorySerializer, CodeSearchItemSerializer
import requests


class RepositorySearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")
        language = request.query_params.get("programming_language", "")
        if not query:
            return Response({"error": 'Query parameter "q" is required'}, status=400)
        try:
            api = Api()
            repository = GithubRepository(api)
            use_case = SearchUseCase(repository)
            results = use_case.execute(query, language=language)

            serializer = RepositorySerializer(results.get("items", []), many=True)
            return Response(serializer.data)
        except requests.exceptions.HTTPError as e:
            print(f"==>> e: {e}")
            if e.response.status_code == 401:
                return Response({"error": "Invalid token"}, status=401)
            return Response({"error": "An error occurred"}, status=500)


class CodeSearchView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")
        if not query:
            return Response({"error": 'Query parameter "q" is required'}, status=400)
        try:
            api = Api()
            repository = GithubRepository(api)
            use_case = SearchCodeUseCase(repository)
            results = use_case.execute(query)

            serializer = CodeSearchItemSerializer(results.get("items", []), many=True)
            return Response(serializer.data)
        except requests.exceptions.HTTPError as e:
            print(f"==>> e: {e}")
            if e.response.status_code == 401:
                return Response({"error": "Invalid token"}, status=401)
            return Response({"error": "An error occurred"}, status=500)
