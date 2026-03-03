import httpx
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from django.urls import reverse
from rest_framework.request import Request

# ==========================================
# 1. INTERFACES (Dependency Inversion Principle)
# ==========================================
class MCPTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def schema(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def execute(self, arguments: Dict[str, Any], request: Request) -> Any:
        pass


class SearchGithubReposTool(MCPTool):
    """Herramienta existente para buscar repositorios."""
    
    @property
    def name(self) -> str:
        return "search_github_repos"

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Busca repositorios en GitHub por nombre, descripción o tema. Útil para encontrar proyectos open source, librerías o herramientas.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Términos de búsqueda para encontrar repositorios (ej: 'machine learning python', 'react framework')"
                        }
                    },
                    "required": ["query"]
                }
            }
        }

    async def execute(self, arguments: Dict[str, Any], request: Request) -> Any:
        query = arguments.get("query", "")
        req_url = request.build_absolute_uri(reverse('repository-search'))
        
        # Convertimos headers a dict para httpx
        headers = {k: v for k, v in request.headers.items()}
        
        # Usamos httpx para llamadas asíncronas
        async with httpx.AsyncClient() as client:
            response = await client.get(req_url, headers=headers, params={"q": query})
            print(f"==>> response: {response}")
            response.raise_for_status()
            res = response.json()
            print('\n┌─ back/apps/chat/mcp_tools.py - repos search\n└─', res)
            return res


class SearchGithubCodeTool(MCPTool):
    """Nueva herramienta para buscar código específico dentro de GitHub."""
    
    @property
    def name(self) -> str:
        return "search_github_code"

    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": "Busca código fuente dentro de GitHub. Permite buscar por término, repositorio, lenguaje, nombre de archivo o ruta.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_term": {"type": "string", "description": "Término exacto o palabra clave a buscar en el código"},
                        "repo": {"type": "string", "description": "Repositorio específico donde buscar (ej: 'encode/django-rest-framework')"},
                        "language": {"type": "string", "description": "Lenguaje de programación (ej: 'python', 'javascript')"},
                        "filename": {"type": "string", "description": "Nombre de archivo específico (ej: 'views.py')"},
                        "extension": {"type": "string", "description": "Extensión del archivo (ej: 'js', 'py')"},
                        "path": {"type": "string", "description": "Ruta dentro del repositorio"}
                    },
                    "required": ["search_term"]
                }
            }
        }

    def _build_search_query(self, kwargs: Dict[str, Any]) -> str:
        """Responsabilidad única: Construir el query string formato GitHub."""
        query_parts = [kwargs.get("search_term", "")]
        
        if kwargs.get("repo"): query_parts.append(f"repo:{kwargs['repo']}")
        if kwargs.get("language"): query_parts.append(f"language:{kwargs['language']}")
        if kwargs.get("filename"): query_parts.append(f"filename:{kwargs['filename']}")
        if kwargs.get("extension"): query_parts.append(f"extension:{kwargs['extension']}")
        if kwargs.get("path"): query_parts.append(f"path:{kwargs['path']}")
            
        return "+".join(query_parts)

    async def execute(self, arguments: Dict[str, Any], request: Request) -> Any:
        query = self._build_search_query(arguments)
        url = "https://api.github.com/search/code"
        
        params = {
            "q": query,
            "per_page": arguments.get("per_page", 10)
        }
        
        headers = {"Accept": "application/vnd.github.v3+json"}
        # Si tienes un token configurado en tu app, agrégalo aquí:
        # headers["Authorization"] = f"Bearer TU_TOKEN"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            
            if response.status_code == 403:
                return {"error": "Límite de peticiones de GitHub excedido (Rate Limit). Intenta de nuevo más tarde."}
                
            response.raise_for_status()
            return response.json()


# ==========================================
# 3. REGISTRO DE HERRAMIENTAS (Open/Closed Principle)
# ==========================================
class ToolRegistry:
    """Gestiona y ejecuta las herramientas disponibles dinámicamente."""
    
    def __init__(self):
        self._tools: Dict[str, MCPTool] = {}

    def register(self, tool: MCPTool) -> None:
        self._tools[tool.name] = tool

    def get_schemas(self) -> List[Dict[str, Any]]:
        return [tool.schema for tool in self._tools.values()]

    async def execute(self, tool_name: str, arguments: Dict[str, Any], request: Request) -> str:
        tool = self._tools.get(tool_name)
        if not tool:
            return json.dumps({"error": f"Tool '{tool_name}' not found"})
            
        try:
            result = await tool.execute(arguments, request)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": f"Execution failed: {str(e)}"})


# ==========================================
# 4. EXPOSICIÓN AL EXTERIOR (Manteniendo las firmas originales)
# ==========================================

# Instanciamos el registro y agregamos las herramientas
registry = ToolRegistry()
registry.register(SearchGithubReposTool())
registry.register(SearchGithubCodeTool())
# Para agregar más en el futuro, solo llamas a: registry.register(NuevaHerramientaTool())

def get_available_tools() -> list:
    """Retorna la lista de herramientas disponibles para el LLM"""
    return registry.get_schemas()

async def execute_tool(tool_name: str, arguments: dict, request: Request) -> str:
    """Ejecuta una herramienta por su nombre a través del registro"""
    return await registry.execute(tool_name, arguments, request)