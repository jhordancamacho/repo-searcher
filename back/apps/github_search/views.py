from rest_framework.views import APIView
from rest_framework.response import Response
from .api.api import Api
from .data.repositories.repository import GithubRepository
from .domain.use_cases.search_use_case import SearchUseCase
from .serializer import RepositorySerializer
import requests
class RepositorySearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=400)
        try:
            api = Api()
            repository = GithubRepository(api)
            use_case = SearchUseCase(repository)
            results = use_case.execute(query)

            serializer = RepositorySerializer(results.get('items', []), many=True)
            return Response(serializer.data)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return Response({'error': 'Invalid token'}, status=401)
            return Response({'error': 'An error occurred'}, status=500)