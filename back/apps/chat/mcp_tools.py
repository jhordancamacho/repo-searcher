import httpx
import json
from django.urls import reverse
from rest_framework.request import Request
import requests

SEARCH_GITHUB_TOOL = {
    "type": "function",
    "function": {
        "name": "search_github_repos",
        "description": "Busca repositorios en GitHub por nombre, descripción o tema. Útil para encontrar proyectos open source, librerías o herramientas.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Términos de búsqueda para encontrar repositorios (ej: 'machine learning python', 'react framework', 'django rest api')"
                }
            },
            "required": ["query"]
        }
    }
}


async def execute_search_github_repos(query: str, request: Request) -> list:
    """
    Ejecuta la búsqueda de repositorios llamando al endpoint /github/search/
    """
    # Construir la URL usando reverse
    req = request.build_absolute_uri(reverse('repository-search'))
    headers = request.headers
    response = requests.get(req, headers=headers, params={"q": query})
    response.raise_for_status()
    res= response.json()
    print('\n┌─ back/apps/chat/mcp_tools.py:41 - res\n└─', res)
    return res


def get_available_tools() -> list:
    """Retorna la lista de herramientas disponibles para el LLM"""
    return [SEARCH_GITHUB_TOOL]


async def execute_tool(tool_name: str, arguments: dict, request: Request) -> str:
    """
    Ejecuta una herramienta por su nombre y retorna el resultado como string JSON
    """
    if tool_name == "search_github_repos":
        result = await execute_search_github_repos(arguments.get("query", ""), request)
        return json.dumps(result, ensure_ascii=False)
    else:
        return json.dumps({"error": f"Tool '{tool_name}' not found"})
