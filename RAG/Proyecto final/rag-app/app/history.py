"""
Histórico de preguntas, persistido en su PROPIA colección de Chroma
(separada de los documentos, para no mezclar cosas). Sobrevive a
reiniciar la API porque usa el mismo cliente persistente que store.py.
"""

import json
import uuid
from datetime import datetime, timezone

import chromadb

from app.store import CHROMA_PATH

HISTORY_COLLECTION_NAME = "historial_preguntas"


def _get_history_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=HISTORY_COLLECTION_NAME)


def save_entry(
    question: str,
    answer: str,
    citations: list[dict],
    abstained: bool,
    vector: list[float],
) -> None:
    """
    Guarda una pregunta/respuesta. Reutiliza el vector que ya se calculó
    para la búsqueda (no hace un embedding aparte solo para el histórico).
    """
    collection = _get_history_collection()
    entry_id = str(uuid.uuid4())
    collection.add(
        ids=[entry_id],
        embeddings=[vector],
        documents=[question],
        metadatas=[
            {
                "answer": answer,
                "citations_json": json.dumps(citations, ensure_ascii=False),
                "abstained": abstained,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ],
    )


def list_history(limit: int = 50) -> list[dict]:
    """Devuelve las últimas `limit` preguntas, de la más antigua a la más reciente."""
    collection = _get_history_collection()
    if collection.count() == 0:
        return []

    datos = collection.get(include=["documents", "metadatas"])
    entradas = []
    for question, metadata in zip(datos["documents"], datos["metadatas"]):
        entradas.append(
            {
                "question": question,
                "answer": metadata["answer"],
                "citations": json.loads(metadata["citations_json"]),
                "abstained": metadata["abstained"],
                "timestamp": metadata["timestamp"],
            }
        )

    entradas.sort(key=lambda e: e["timestamp"])
    return entradas[-limit:]