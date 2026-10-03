"""
Usa gemini-embedding-001 de Google AI para incrustar documentos y preguntas del usuario.
Requiere GOOGLE_API_KEY en el archivo .env (ver .env.example).
Consigue tu clave en https://aistudio.google.com/apikey
"""

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.types import EmbedContentConfig

load_dotenv()

MODEL = "gemini-embedding-001"
OUTPUT_DIM = 768  

_client: genai.Client | None = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Falta GOOGLE_API_KEY. Copia .env.example a .env y pega tu clave "
                "de https://aistudio.google.com/apikey"
            )
        _client = genai.Client(api_key=api_key)
    return _client


def _embed_con_reintentos(client: genai.Client, contents: list[str], task_type: str, max_reintentos: int = 4):
    """
    Llama a embed_content con reintentos y espera creciente si Google
    responde 429 (límite de peticiones por minuto alcanzado). No hace
    nada especial ante otros errores (esos se propagan tal cual).
    """
    for intento in range(max_reintentos):
        try:
            return client.models.embed_content(
                model=MODEL,
                contents=contents,
                config=EmbedContentConfig(task_type=task_type, output_dimensionality=OUTPUT_DIM),
            )
        except Exception as e:
            es_limite = "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e)
            if not es_limite or intento == max_reintentos - 1:
                raise
            espera = 20 * (intento + 1)  # 20s, 40s, 60s, 80s
            print(f"[embed] límite de peticiones alcanzado, esperando {espera}s (intento {intento + 1}/{max_reintentos})...")
            time.sleep(espera)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """
    Incrusta una lista de chunks que se van a guardar en el índice.
    Se manda en lotes porque la API de Google rechaza más de 100 textos
    por llamada, y cada lote reintenta con espera si se topa con el
    límite de peticiones por minuto (free tier).
    """
    client = get_client()
    BATCH_SIZE = 100
    vectors: list[list[float]] = []

    for i in range(0, len(texts), BATCH_SIZE):
        lote = texts[i : i + BATCH_SIZE]
        response = _embed_con_reintentos(client, lote, task_type="RETRIEVAL_DOCUMENT")
        vectors.extend(e.values for e in response.embeddings)
        time.sleep(1)  # pequeña pausa entre lotes para no ráfaguear la cuota

    return vectors


def embed_query(text: str) -> list[float]:
    """Incrusta una pregunta del usuario. Mismo modelo/dimensiones que embed_documents."""
    client = get_client()
    response = _embed_con_reintentos(client, [text], task_type="RETRIEVAL_QUERY")
    return response.embeddings[0].values


if __name__ == "__main__":
    import math

    def cosine(a: list[float], b: list[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        return dot / (na * nb)

    docs = [
        "El gato duerme en el sofá durante toda la tarde.",
        "El felino descansa en el mueble de la sala.",
        "La bolsa de valores subió hoy por la mañana.",
    ]
    vectors = embed_documents(docs)
    print(f"Dimensión de cada vector: {len(vectors[0])}")

    sim_relacionadas = cosine(vectors[0], vectors[1])
    sim_no_relacionadas = cosine(vectors[0], vectors[2])
    print(f"Similitud entre frases relacionadas:     {sim_relacionadas:.3f}")
    print(f"Similitud entre frases no relacionadas:  {sim_no_relacionadas:.3f}")

    if sim_relacionadas > sim_no_relacionadas:
        print("Bien: las frases relacionadas quedaron más cerca entre sí.")
    else:
        print("Algo no cuadra — revisa el modelo o la clave antes de seguir.")