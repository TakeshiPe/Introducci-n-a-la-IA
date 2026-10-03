"""
Alternativa a embed.py: embeddings LOCALES, sin llamadas a ninguna API,
por lo tanto sin límite de RPM/RPD ni costo, salida de emergencia para documentos 
grandes en plan gratuito.

Usa un modelo de sentence-transformers multilingüe (sirve bien para
español). La primera vez que lo uses va a descargar el modelo
(~470 MB) desde HuggingFace; después queda en caché local.

Para usarlo en vez de Google AI:
1. `pip install sentence-transformers`
2. En main.py, cambia:
     from app.embed import embed_documents, embed_query
   por:
     from app.embed_local import embed_documents, embed_query
3. En store.py, cambia OUTPUT_DIM si lo tienes fijo en otro lado — este
   modelo da vectores de 384 dimensiones, no 768 como Gemini.
4. IMPORTANTE: borra la carpeta chroma/ antes de reingestar. Igual que
   pasó al mezclar dimensión 3 con 768, no puedes mezclar 384 con 768
   en la misma colección.
5. Documenta en tu README que para este corpus (documentos largos) se
   usó un embedder local en vez de Google AI, y por qué (límite de
   cuota del plan gratuito), citando la autorización de tu profesor —
   el enunciado original pide Google AI como única fuente, así que esta
   desviación debe quedar explícita y justificada en el reporte.
"""

OUTPUT_DIM = 384
_MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(_MODEL_NAME)
    return _model


def embed_documents(texts: list[str]) -> list[list[float]]:
    model = _get_model()
    vectors = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    return embed_documents([text])[0]