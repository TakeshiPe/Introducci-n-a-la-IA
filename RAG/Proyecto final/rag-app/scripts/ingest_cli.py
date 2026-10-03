"""
Indexa documentos directamente desde la terminal, sin pasar por
FastAPI ni Streamlit. Útil para documentos grandes que, por los
reintentos de la cuota gratuita de Google, pueden tardar varios
minutos: así no los corta el timeout del navegador ni el de Streamlit.

Uso (desde la raíz de rag-app/):
    python scripts/ingest_cli.py data/archivo.pdf
    python scripts/ingest_cli.py data/archivo1.pdf data/archivo2.pdf data/archivo3.pdf
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.chunk import chunk_file  # noqa: E402
from app.embed_local import embed_documents  # noqa: E402
from app.store import add_chunks  # noqa: E402


def ingest_path(path: str) -> None:
    print(f"\n=== Indexando {path} ===")
    chunks = chunk_file(path)
    print(f"  {len(chunks)} chunks generados")
    if not chunks:
        print("  (documento vacío, se omite)")
        return

    print("  Generando embeddings (puede tardar varios minutos si hay reintentos)...")
    vectors = embed_documents([c.text for c in chunks])
    add_chunks(chunks, vectors)
    print(f"  Listo: {len(chunks)} chunks indexados desde {os.path.basename(path)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/ingest_cli.py archivo1.pdf [archivo2.pdf ...]")
        sys.exit(1)

    for ruta in sys.argv[1:]:
        try:
            ingest_path(ruta)
        except Exception as e:
            print(f"  ERROR con {ruta}: {e}")

    print("\nTerminado.")