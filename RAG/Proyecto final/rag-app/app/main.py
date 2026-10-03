"""
API: /health, /ingest, /query, /sources, /history.
"""

import asyncio
import os
import tempfile

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.chunk import chunk_file
from app.embed_local import embed_documents, embed_query
from app.errors import humanize_error
from app.generate import generate_answer
from app.history import list_history, save_entry
from app.store import add_chunks, get_collection, list_sources
from app.store import query as store_query

app = FastAPI(title="RAG de leyes mexicanas")

# Streamlit (8501) necesita poder llamar a esta API (8000) desde el navegador.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    try:
        collection = get_collection()
        return {"status": "ok", "chroma_ok": True, "chunks_indexados": collection.count()}
    except Exception as e:
        return {"status": "ok", "chroma_ok": False, "error": humanize_error(e)}


@app.get("/sources")
def sources():
    """Lista los documentos (source) ya indexados, para poder filtrar por uno."""
    try:
        return {"sources": list_sources()}
    except Exception as e:
        return {"sources": [], "error": humanize_error(e)}


@app.get("/history")
def history(limit: int = 50):
    """Histórico de preguntas, persistido en Chroma (sobrevive a reiniciar la API)."""
    try:
        return {"history": list_history(limit=limit)}
    except Exception as e:
        return {"history": [], "error": humanize_error(e)}


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    """
    Indexa UN archivo por llamada (más simple y confiable desde /docs
    que subir varios a la vez). Si tienes varios documentos, llama a
    este endpoint una vez por archivo — la UI de Streamlit hace ese
    bucle por ti automáticamente.
    """
    try:
        content = await file.read()
        suffix = os.path.splitext(file.filename or "documento.txt")[1] or ".txt"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode="wb") as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # asyncio.to_thread: estas llamadas son bloqueantes (CPU/disco);
            # sin esto, mientras indexan, TODA la API se congela (incluido
            # /health y /sources) porque este endpoint es `async`.
            chunks = await asyncio.to_thread(chunk_file, tmp_path)
            # chunk_file usa el nombre del archivo temporal como `source`;
            # lo corregimos para que quede el nombre real del archivo subido.
            for c in chunks:
                c.source = file.filename or c.source

            chunks_indexados = 0
            if chunks:
                vectors = await asyncio.to_thread(embed_documents, [c.text for c in chunks])
                await asyncio.to_thread(add_chunks, chunks, vectors)
                chunks_indexados = len(chunks)
        finally:
            os.unlink(tmp_path)

        return {
            "documento": file.filename,
            "chunks_indexados": chunks_indexados,
            "error": None,
        }

    except Exception as e:
        return {"documento": file.filename, "chunks_indexados": 0, "error": humanize_error(e)}


class QueryRequest(BaseModel):
    question: str
    top_k: int = 3
    source: str | None = None  # si viene, solo busca dentro de ese documento


@app.post("/query")
def query_endpoint(payload: QueryRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=422, detail="La pregunta no puede estar vacía")

    try:
        vector = embed_query(payload.question)
    except Exception as e:
        # Nunca un 500 crudo: devolvemos un mensaje claro y abstained=True.
        return {"answer": humanize_error(e), "citations": [], "abstained": True}

    hits = store_query(vector, top_k=payload.top_k, source=payload.source)

    if not hits:
        mensaje = (
            f"No tengo evidencia suficiente para responder (sin chunks parecidos en '{payload.source}')."
            if payload.source
            else "No tengo evidencia suficiente para responder (el índice está vacío o no hay chunks parecidos)."
        )
        return {"answer": mensaje, "citations": [], "abstained": True}

    try:
        answer, abstained = generate_answer(payload.question, hits)
    except Exception as e:
        return {"answer": humanize_error(e), "citations": hits, "abstained": True}

    # Se guarda en el histórico persistente (no rompe la respuesta si falla).
    try:
        save_entry(payload.question, answer, hits, abstained, vector)
    except Exception:
        pass

    return {"answer": answer, "citations": hits, "abstained": abstained}