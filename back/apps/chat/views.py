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
            tools_description = "\n".join(
                [
                    f"- {tool['function']['name']}: {tool['function']['description']}"
                    for tool in available_tools
                ]
            )

            output_schema = ChatOutput.model_json_schema()

            messages = [
                {
                    "role": "system",
                    "content": f"Eres un asistente útil para búsquedas en GitHub.\n"
                    f"Herramientas disponibles:\n{tools_description}\n"
                    f"Usa las herramientas apropiadas cuando sea necesario. "
                    f"Tu respuesta final DEBE ser exclusivamente un JSON válido que cumpla con este schema:\n"
                    f"{json.dumps(output_schema, ensure_ascii=False)}\n"
                    f"No incluyas texto fuera del JSON. Responde en español.",
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
                    messages.append(assistant_message)

                    for tool_call in assistant_message.tool_calls:
                        tool_name = tool_call.function.name

                        try:
                            tool_args = json.loads(tool_call.function.arguments or "{}")
                        except json.JSONDecodeError:
                            tool_args = {}

                        tool_result = loop.run_until_complete(
                            execute_tool(tool_name, tool_args, request)
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
