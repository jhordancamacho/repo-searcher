import json
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
from .mcp_tools import get_available_tools, execute_tool


class ChatView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt', '')
        
        if not prompt:
            return Response(
                {'error': 'El campo "prompt" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Configurar cliente OpenAI
            client = OpenAI(
                api_key=settings.LLM_BINDING_API_KEY,
                base_url=settings.LLM_BINDING_HOST if settings.LLM_BINDING_HOST else None
            )
            
            messages = [
                {
                    "role": "system",
                    "content": "Eres un asistente útil que ayuda a buscar repositorios en GitHub. "
                               "Usa la herramienta search_github_repos cuando el usuario quiera encontrar "
                               "repositorios, proyectos o librerías. Responde en español."
                },
                {"role": "user", "content": prompt}
            ]
            
            # Primera llamada al LLM
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                tools=get_available_tools(),
                tool_choice="auto"
            )
            
            assistant_message = response.choices[0].message
            
            # Si el LLM quiere usar herramientas
            if assistant_message.tool_calls:
                messages.append(assistant_message)
                
                # Ejecutar cada herramienta
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    # Ejecutar la herramienta de forma async
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        tool_result = loop.run_until_complete(
                            execute_tool(tool_name, tool_args,request)
                        )
                    finally:
                        loop.close()
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                
                # Segunda llamada al LLM con los resultados
                final_response = client.chat.completions.create(
                    model=settings.LLM_MODEL,
                    messages=messages
                )
                
                final_content = final_response.choices[0].message.content
            else:
                final_content = assistant_message.content
            
            return Response({
                'response': final_content,
                'prompt': prompt
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
