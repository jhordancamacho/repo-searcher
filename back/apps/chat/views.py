import json
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI
from .mcp_tools import get_available_tools, execute_tool
from .schemas import BodyParams, ChatOutput


class ChatView(APIView):
    def post(self, request: BodyParams):
        prompt = request.data.get("prompt")
        programming_language = request.data.get("programming_language", None)
        if not prompt:
            return Response(
                {"error": 'El campo "prompt" es requerido'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Configurar cliente OpenAI
            client: OpenAI = OpenAI(
                api_key=settings.LLM_BINDING_API_KEY,
                base_url=settings.LLM_BINDING_HOST
                if settings.LLM_BINDING_HOST
                else None,
            )

            # Construir mensaje del sistema dinámicamente basado en herramientas disponibles
            available_tools = get_available_tools()

            output_schema = ChatOutput.model_json_schema()

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Eres un asistente experto en búsquedas de código en GitHub y desarrollador Senior.\n"
                        "WORKFLOW OBLIGATORIO:\n"
                        "1. Analiza el prompt del usuario y utiliza la herramienta 'github_deep_search' "
                        "generando 'repo_queries' y 'code_queries' optimizados.\n"
                        "2. Al recibir los resultados (que incluyen READMEs), evalúa semánticamente cuál cumple mejor "
                        "con los requisitos y verifica su madurez.\n"
                        "3. Tu respuesta final DEBE ser un JSON válido que cumpla con este schema:\n"
                        f"{json.dumps(output_schema, ensure_ascii=False)}\n"
                        "REGLA DE RESPUESTA:\n"
                        "- El primer elemento de 'repositories' DEBE ser el proyecto GANADOR.\n"
                        "- En el campo 'description' del ganador, incluye una breve JUSTIFICACIÓN de por qué fue seleccionado.\n"
                        "- Los siguientes 3 elementos deben ser las MENCIONES HONORÍFICAS.\n"
                        "Responde en español. No incluyas texto fuera del JSON."
                    ),
                },
                {
                    "role": "user",
                    "content": f"{prompt}"
                    + (
                        f" (lenguaje: {programming_language})"
                        if programming_language
                        else ""
                    ),
                },
            ]
            # Permite múltiples rondas de tools: repos -> code -> repos -> ...
            max_tool_rounds = 6
            tool_rounds = 0

            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=messages,
                tools=available_tools,
                tool_choice="auto",
            )
            assistant_message = response.choices[0].message

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                while assistant_message.tool_calls and tool_rounds < max_tool_rounds:
                    tool_rounds += 1
                    print("\n┌─ apps/chat/views.py:80 - tool_rounds\n└─", tool_rounds)
                    messages.append(assistant_message)

                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name
                        print("\n┌─ apps/chat/views.py:84 - tool_name\n└─", tool_name)

                        try:
                            tool_args = json.loads(tool_call.function.arguments or "{}")
                            print(
                                "\n┌─ apps/chat/views.py:87 - tool_args\n└─", tool_args
                            )
                        except json.JSONDecodeError:
                            print(
                                "\n┌─ apps/chat/views.py:89 - json.JSONDecodeError\n└─"
                            )
                            tool_args = {}

                        tool_result = loop.run_until_complete(
                            execute_tool(tool_name, tool_args, request)
                        )
                        print(
                            "\n┌─ apps/chat/views.py:96 - tool_result\n└─", tool_result
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": tool_result,
                            }
                        )
                    # Siguiente ronda: el LLM decide si necesita más tools o responde
                    response = client.chat.completions.create(
                        model=settings.LLM_MODEL,
                        messages=messages,
                        tools=available_tools,
                        tool_choice="auto",
                    )
                    assistant_message = response.choices[0].message
            finally:
                loop.close()

            final_content = assistant_message.content

            try:
                parsed = ChatOutput.model_validate_json(final_content)
            except Exception:
                # Si el LLM envuelve el JSON en markdown, intentar extraerlo
                import re

                match = re.search(r"\{.*\}", final_content, re.DOTALL)
                if match:
                    parsed = ChatOutput.model_validate_json(match.group())
                else:
                    raise ValueError("La respuesta del modelo no contiene JSON válido")

            return Response(
                {"response": parsed.model_dump(mode="json"), "prompt": prompt}
            )

        except Exception as e:
            print("\n┌─ apps/chat/views.py:97 - e\n└─", e)
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
