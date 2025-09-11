from rest_framework.views import APIView
from rest_framework.response import Response
from .api.api import Api
from .data.repositories.repository import GithubRepository
from .domain.use_cases.search_use_case import SearchUseCase
from .serializer import RepositorySerializer

class RepositorySearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=400)

        api = Api()
        repository = GithubRepository(api)
        use_case = SearchUseCase(repository)
        results = use_case.execute(query)

        serializer = RepositorySerializer(results.get('items', []), many=True)
        return Response(serializer.data)