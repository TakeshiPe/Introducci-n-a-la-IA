# RAG

Chatbot de consulta de documentos normativos en materia de PLD/FT en México, a través de un sistema RAG.

## Configuración

```bash
cd "RAG/Proyecto final/rag-app"
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows (PowerShell):

```powershell
cd "RAG/Proyecto final/rag-app"
python3 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Futuras sesiones: activar el `venv` nuevamente y posterior correr los programas. 

Se desactiva con `deactivate`.

## Programas

Para la construcción del chatbot se desarrollaron los siguientes programas:

| Archivo | Descripción |
|---|---|
| `chunk.py` | Parte el texto largo en chunks |
| `embed_local.py` | Realiza embeddings localmente sin utilizar API |
| `embed.py` | Realiza embeddings a través de Gemini | 
| `errors.py` | Traduce errores técnicos a mensajes claros para el usuario | 
| `generate.py` | Genera la respuesta con Gemini | 
| `history.py` | Histórico de preguntas | 
| `main.py` | API: /health, /ingest, /query, /sources, /history | 
| `store.py` | Guarda vectores |
| `ingest_cli.py` | Indexa documentos directamente desde la terminal |
| `streamlit_app.py` | Interfaz de la aplicación |

## Configuración de GOOGLE_API_KEY

Copia `.env.example` a `.env` y coloca tu clave de [Google AI Studio](https://aistudio.google.com/apikey) en `GOOGLE_API_KEY=`.

## Ejecución

Para utilizar la aplicaciónse coloca en la terminal:

`uvicorn app.main:app --reload --port 8000`

Posterioremnte en otra terminal se ejecuta:

`streamlit run ui/streamlit_app.py`

La aplicación se abrirá automáticamente en el explorador.

## Elegir el corpus

Los documentos se indexan mediante la aplicación en la primera sección (**1. Cargar documentos**), se selecciona el botón de `Upload`, los documentos se encuentran en 

```
rag-app/data
```

Posteriormente se hace clic en el botón que dice _Indexar documentos_. Una vez indexados los documentos, en el lado izquierdo aparecerá el número de chunks indexados.

### Embeddings

Se tienen 3 programas para realizar embeddings (`embed_local.py`, `embed.py` e `ingest_cli.py`). El primero es el utilizado por la aplicación, mientras que el segundo fue creado durante la construcción inicial, este programa se ve limitado a 100 Peticiones Por Minuto, por lo que no fue posible realizar los embeddings de todos los documentos.

El último programa realiza los embeddings de forma local desde la terminal, se recomienda utilizarlo cuando se tengan documentos grandes que tardan mucho desde la UI, para ejecutarlo se requiere:

```
python scripts/ingest_cli.py data/nombre_de_ley.pdf
```

## Configuración de búsqueda

Permite segmentar la pregunta realizada al chatbot mediante los siguientes parámetros:

* Chunks a recuperar por pregunta (_top\_k_): Limita la búsqueda a un determinado número de chunks. Se puede elegir entre 1 y 8 chunks,
* Buscar sólo en un documento: Limita la búsqueda a una sola fuente.

## Histórico de preguntas

En este apartado se irán gurdando las preguntas que el usuario haga en el chatbot, permitiendo acceder a ellas más rápidamente. 

## Hacer preguntas

En este apartado el usuario puede hacer uso de la aplicación, escribiendo la pregunta al chatbot. La respuesta puede demorar en función de si los servidores de Google estén saturados.

## Terminar sesión

Para terminar la sesión que se esté ejecutando, el método principal es hacer clic dentro de las ventanas de la terminal que estén ejecutando `uvicorn` y `streamlit` (una a la vez) y presionar `Ctrl + C`. Esto interrumpirá el servidor de forma segura.

## Prueba de preguntas

Para probar la aplicación, se introduce la siguiente pregunta:

```
¿De cuánto debe ser la comercialización de vehículos nuevos o usados para ser considerada como actividad vulnerable?
```

A lo que el programa responde lo siguiente:

```
Para ser considerada como actividad vulnerable, la comercialización o distribución habitual o profesional de vehículos, nuevos o usados (ya sean aéreos, marítimos o terrestres), debe tener un valor igual o superior al equivalente a tres mil doscientas diez veces el valor diario de la UMA [1].
```

En el [Reporte](Reporte.md) se incluye el listado de preguntas hechas a modo de prueba, así como una pregunta fuera de dominio, para validar la respuesta generada por el chatbot.