
### Paso 1: Traducción de Intención a Queries (LLM)
El objetivo aquí es estructurar la petición del usuario en consultas que la API de GitHub entienda.
* **Actor:** LLM (Gemini).
* **Entrada:** El prompt del usuario (ej. *"proyecto de fastapi que usen el api de claude"*).
* **Instrucción al LLM:** Pídele que genere un objeto JSON estricto con dos listas de strings: `repo_queries` y `code_queries`.
* **Salida esperada:**
    ```json
    {
      "repo_queries": ["fastapi claude language:python"],
      "code_queries": [
        "anthropic fastapi in:file filename:requirements.txt",
        "anthropic fastapi in:file filename:pyproject.toml",
        "import anthropic fastapi in:file extension:py"
      ]
    }
    ```

### Paso 2: Ejecución de la Búsqueda Dual (API de GitHub)
Tu script toma el JSON del paso anterior y dispara las peticiones HTTP.
* **Actor:** Tu script base (Python).
* **Acción A (Búsqueda por Código):** Itera sobre la lista de `code_queries` y haz peticiones GET a `https://api.github.com/search/code?q={query}`. Extrae de los resultados el `repository.full_name` (ej. `usuario/repo`).
* **Acción B (Búsqueda por Repositorio):** Itera sobre la lista de `repo_queries` y haz peticiones GET a `https://api.github.com/search/repositories?q={query}`. Extrae también el `full_name`.

### Paso 3: Agrupación y Puntuación Base (Script)
La API de GitHub te devolverá muchos resultados sueltos y duplicados que necesitas limpiar.
* **Actor:** Tu script base.
* **Acción:**
    1.  Une los resultados del Paso 2A y 2B en una sola lista y elimina los nombres de repositorios duplicados.
    2.  Haz una petición a `https://api.github.com/repos/{full_name}` para cada uno (o usa GraphQL si quieres optimizar las llamadas) para obtener sus metadatos: `stargazers_count`, `forks_count` y `updated_at`.
    3.  Ordena la lista de mayor a menor relevancia (por ejemplo, dándole peso a las estrellas y a la actividad reciente).
    4.  Corta la lista y quédate **estrictamente con el Top 5 o Top 10**.

### Paso 4: Extracción del Contexto Profundo (API de GitHub)
Para que el LLM pueda tomar la decisión final, necesita leer de qué trata cada proyecto finalista.
* **Actor:** Tu script base.
* **Acción:** Por cada repositorio en tu Top 10, haz una petición GET a `https://api.github.com/repos/{full_name}/readme`.
* **Procesamiento:** Decodifica el contenido (suele venir en Base64), recórtalo si es absurdamente largo (para no saturar el contexto) y guárdalo en un diccionario asociándolo al nombre del repositorio.

### Paso 5: Evaluación Semántica y Selección (LLM)
Este es el cierre del embudo, donde delegas la decisión final a la capacidad de razonamiento del modelo.
* **Actor:** LLM (Gemini).
* **Entrada:** El prompt original del usuario + el bloque de texto con los READMEs recopilados en el Paso 4.
* **Instrucción al LLM:** *"El usuario solicitó: [Prompt]. Aquí tienes los READMEs de los 10 mejores candidatos encontrados en GitHub. Actúa como un desarrollador Senior, evalúa cuál cumple mejor con los requisitos, verifica la madurez del proyecto según su documentación y devuelve el repositorio ganador junto con una breve justificación y un top 3 de menciones honoríficas."*
* **Salida final:** Tu script imprime la respuesta del LLM directamente en la terminal.
