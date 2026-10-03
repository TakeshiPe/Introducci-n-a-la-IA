"""
Importante: Chroma puede generar sus propios embeddings por defecto, pero
en este proyecto NO se usa esa función. Los vectores se pasan explícitamente en
`add()` / `query()`.
"""

import chromadb

CHROMA_PATH = "chroma"
COLLECTION_NAME = "documentos"


def get_collection():
    """
    Abre (o crea si no existe) la colección persistente en disco.
    Se configura para distancia coseno, que combina bien con embeddings
    de texto como los de Gemini.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def add_chunks(chunks, vectors: list[list[float]]) -> None:
    """
    Guarda una lista de Chunk (de chunk.py) junto con sus vectores
    (de embed.py). El id de cada chunk se arma con `source` + `index`
    para que sea estable y legible.
    """
    if len(chunks) != len(vectors):
        raise ValueError("chunks y vectors deben tener la misma longitud")
    if not chunks:
        return

    collection = get_collection()
    ids = [f"{c.source}::{c.index}" for c in chunks]
    documents = [c.text for c in chunks]
    metadatas = [{"source": c.source, "chunk_index": c.index} for c in chunks]

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas,
    )


def query(vector: list[float], top_k: int = 3, source: str | None = None) -> list[dict]:
    """
    Busca los `top_k` chunks más cercanos al vector de la pregunta.
    Si `source` viene con un valor, solo busca dentro de ese documento.
    Devuelve una lista de dicts: {text, source, chunk_index, score}.
    `score` va de 0 a 1 (más alto = más parecido).
    """
    collection = get_collection()
    if collection.count() == 0:
        return []

    where = {"source": source} if source else None
    result = collection.query(
        query_embeddings=[vector],
        n_results=min(top_k, collection.count()),
        where=where,
    )

    hits = []
    for text, metadata, distance in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        score = 1 - distance  # con hnsw:space="cosine", distance = 1 - similitud
        hits.append(
            {
                "text": text,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "score": round(score, 4),
            }
        )
    return hits


def list_sources() -> list[str]:
    """Devuelve la lista (sin duplicados, ordenada) de `source` ya indexados."""
    collection = get_collection()
    if collection.count() == 0:
        return []
    datos = collection.get(include=["metadatas"])
    fuentes = {m["source"] for m in datos["metadatas"]}
    return sorted(fuentes)


if __name__ == "__main__":
    collection = get_collection()
    print(f"Chunks actualmente en el índice: {collection.count()}")

    if collection.count() == 0:
        from app.chunk import Chunk

        chunks_falsos = [
            Chunk(text="El sol es una estrella de tipo G.", source="demo.txt", index=0),
            Chunk(text="La Luna es el satélite natural de la Tierra.", source="demo.txt", index=1),
        ]
        vectores_falsos = [
            [1.0, 0.0, 0.0],
            [0.9, 0.1, 0.0],
        ]
        add_chunks(chunks_falsos, vectores_falsos)
        print("Agregados 2 chunks de prueba. Vuelve a correr este script.")
    else:
        resultados = query([1.0, 0.0, 0.0], top_k=2)
        print("Resultados de la consulta:")
        for r in resultados:
            print(f"  score={r['score']}  fuente={r['source']}  texto={r['text']}")