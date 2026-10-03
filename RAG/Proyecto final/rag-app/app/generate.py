"""
Genera la respuesta con Gemini, anclada a los chunks recuperados,
y decidir cuándo abstenerse.

Dos capas de abstención:
1. Por score: si el mejor chunk recuperado tiene un score menor a
   MIN_SCORE, ni siquiera se llama a Gemini — no hay evidencia parecida.
2. Por el propio modelo: aunque el score pase el umbral, los chunks
   recuperados podrían no contener la respuesta real. Se le instruye a
   Gemini que diga literalmente NO_EVIDENCE_MSG si pasa eso, y el código
   detecta esa frase para marcar `abstained=True`.
"""

import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

# Alias que Google mantiene apuntando al Flash estable vigente, para no
# tener que actualizar el nombre del modelo a mano cada vez que sacan
# una versión nueva.
MODEL = "gemini-flash-latest"

MIN_SCORE = 0.5

NO_EVIDENCE_MSG = "No cuento con evidencia suficiente en el corpus para responder esta pregunta."

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("Falta GOOGLE_API_KEY en el archivo .env")
        _client = genai.Client(api_key=api_key)
    return _client


def _build_prompt(question: str, hits: list[dict]) -> str:
    evidencia = "\n\n".join(
        f"[{i + 1}] (Fuente: {h['source']}) {h['text']}" for i, h in enumerate(hits)
    )
    return f"""Eres un asistente de inteligencia artificial especializado en consultoría jurídica,
    legal y normativa. Tu objetivo principal es responder a las preguntas del usuario usando ÚNICAMENTE la evidencia
entregada abajo. No uses conocimiento propio ni información fuera de esta evidencia.

Evidencia recuperada:
{evidencia}

Pregunta del usuario:
{question}

Instrucciones:
- Responde en español, de forma clara y directa.
- Limita tus respuestas estrictamente a la evidencia o corpus entregada arriba. No inventes información ni uses conocimiento propio.
- Cada afirmación debe ir acompañada de su cita entre corchetes, por ejemplo [1] o [2].
- Si la evidencia de arriba NO contiene información suficiente para responder la
  pregunta, responde EXACTAMENTE con esta frase y nada más: "{NO_EVIDENCE_MSG}"
- No extrapoles, no supongas, no interpretes más allá de lo escrito y no utilices conocimiento jurídico externo o general que no esté respaldado por los documentos de referencia."
"""


def _generate_con_reintentos(client: genai.Client, prompt: str, max_reintentos: int = 3):
    """Reintenta con espera creciente si Google responde 429/503 (saturado)."""
    for intento in range(max_reintentos):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt)
        except Exception as e:
            texto = str(e)
            es_transitorio = any(x in texto for x in ("429", "503", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))
            if not es_transitorio or intento == max_reintentos - 1:
                raise
            espera = 10 * (intento + 1)  # 10s, 20s, 30s
            print(f"[generate] Google saturado, esperando {espera}s (intento {intento + 1}/{max_reintentos})...")
            time.sleep(espera)


def generate_answer(question: str, hits: list[dict]) -> tuple[str, bool]:
    """
    Devuelve (answer, abstained). No llama a Gemini si ya no hay
    evidencia suficiente por score (ver MIN_SCORE).
    """
    if not hits or hits[0]["score"] < MIN_SCORE:
        return NO_EVIDENCE_MSG, True

    prompt = _build_prompt(question, hits)
    client = get_client()
    response = _generate_con_reintentos(client, prompt)
    answer = (response.text or "").strip()

    abstained = NO_EVIDENCE_MSG.lower() in answer.lower()
    return answer, abstained


if __name__ == "__main__":
    hits_prueba = [
        {
            "text": "La fotosíntesis convierte energía luminosa en energía química en los cloroplastos.",
            "source": "fotosintesis.txt",
            "chunk_index": 0,
            "score": 0.9,
        },
    ]
    answer, abstained = generate_answer("¿Qué es la fotosíntesis?", hits_prueba)
    print(f"abstained={abstained}")
    print(answer)

    print("\n--- Ahora una pregunta sin evidencia (score bajo) ---")
    hits_sin_evidencia = [{**hits_prueba[0], "score": 0.1}]
    answer2, abstained2 = generate_answer("¿Cuál es la capital de Francia?", hits_sin_evidencia)
    print(f"abstained={abstained2}")
    print(answer2)