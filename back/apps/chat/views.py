import json
import asyncio
from typing import List
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
from .mcp_tools import get_available_tools, execute_tool
from .schemas import OutputSchema, ChatOutput, BodyParams

class ChatView(APIView):
    def post(self, request: BodyParams):
        prompt = request.data.get("prompt")
        programming_language = request.data.get("programming_language", None)
        if not prompt:
            return Response(
                {'error': 'El campo "prompt" es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Configurar cliente OpenAI
            client : OpenAI = OpenAI(
                api_key=settings.LLM_BINDING_API_KEY,
                base_url=settings.LLM_BINDING_HOST if settings.LLM_BINDING_HOST else None,

            )
            
            # Construir mensaje del sistema dinámicamente basado en herramientas disponibles
            available_tools = get_available_tools()
            tools_description = "\n".join([
                f"- {tool['function']['name']}: {tool['function']['description']}"
                for tool in available_tools
            ])
            
            messages = [
                {
                    "role": "system",
                    "content": f"Eres un asistente útil para búsquedas en GitHub.\n"
                               f"Herramientas disponibles:\n{tools_description}\n"
                               f"Usa las herramientas apropiadas cuando sea necesario. "
                               f"Responde en español."
                },
                {"role": "user", "content": f"{prompt}" + (f" (lenguaje: {programming_language})" if programming_language else "")}
            ]
            
            # Primera llamada al LLM con tools (usa create, no parse)
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                tools=get_available_tools(),
                tool_choice="auto",
            )
            
            assistant_message = response.choices[0].message
            
            # Si el LLM quiere usar herramientas
            if assistant_message.tool_calls:
                messages.append(assistant_message)
                
                # Ejecutar cada herramienta
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    print(f"==>> tool_name: {tool_name}")
                    tool_args = json.loads(tool_call.function.arguments)
                    print(f"==>> tool_args: {tool_args}")
                    
                    # Ejecutar la herramienta de forma async
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        tool_result = loop.run_until_complete(
                            execute_tool(tool_name, tool_args, request)
                        )
                        print(f"==>> tool_result: {tool_result}")
                    finally:
                        loop.close()
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
                
                # Segunda llamada al LLM con response_format para obtener JSON estructurado
                final_response = client.chat.completions.parse(
                    model=settings.LLM_MODEL,
                    messages=messages,
                    response_format=ChatOutput,
                )
                
                parsed = final_response.choices[0].message.parsed
                if parsed:
                    final_content = parsed.model_dump(mode='json')
                else:
                    final_content = final_response.choices[0].message.content
            else:
                final_content = assistant_message.content
            
            return Response({
                'response': final_content,
                'prompt': prompt
            })
            
        except Exception as e:
            print('\n┌─ apps/chat/views.py:97 - e\n└─', e)
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
