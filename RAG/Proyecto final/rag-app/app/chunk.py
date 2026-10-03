# Dividir texto en chunks de tamaño aproximado, respetando oraciones completas y
# permitiendo un overlap de oraciones entre chunks consecutivos.

import os
import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    source: str
    index: int  # posición del chunk dentro del documento (0, 1, 2...)


def split_paragraphs(text: str) -> list[str]:
    """Divide por líneas en blanco (uno o más saltos de línea vacíos)."""
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def split_sentences(text: str) -> list[str]:
    """
    Divide un párrafo en oraciones. Corta después de '.', '!' o '?' seguido de espacio 
    y una letra mayúscula (o comilla/signo de apertura), para no cortar abreviaturas o 
    números decimales en cualquier punto.
    """
    text = " ".join(text.split())  # normaliza espacios/saltos de línea internos
    if not text:
        return []
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÑ¿¡"])', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(
    text: str,
    source: str,
    chunk_size: int = 200,
    overlap_sentences: int = 2,
) -> list[Chunk]:
    """
    Parte `text` en chunks de ~chunk_size palabras, respetando oraciones
    completas. `overlap_sentences` oraciones se repiten al inicio del
    siguiente chunk para dar continuidad.
    """
    all_sentences: list[str] = []
    for paragraph in split_paragraphs(text):
        all_sentences.extend(split_sentences(paragraph))

    if not all_sentences:
        return []

    chunks: list[Chunk] = []
    current: list[str] = []
    current_words = 0
    index = 0

    for sentence in all_sentences:
        sentence_words = len(sentence.split())

        # Si agregar esta oración se pasa del tamaño y ya hay contenido,
        # cerramos el chunk actual antes de seguir.
        if current and current_words + sentence_words > chunk_size:
            chunks.append(Chunk(text=" ".join(current), source=source, index=index))
            index += 1
            overlap = current[-overlap_sentences:] if overlap_sentences > 0 else []
            current = list(overlap)
            current_words = sum(len(s.split()) for s in current)

        current.append(sentence)
        current_words += sentence_words

    if current:
        chunks.append(Chunk(text=" ".join(current), source=source, index=index))

    return chunks


def extract_text(path: str) -> str:
    """
    Lee el contenido de un archivo. Soporta .txt/.md (texto plano) y
    .pdf (extrae el texto de cada página con pypdf).
    """
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(path)
        paginas = [page.extract_text() or "" for page in reader.pages]
        texto = "\n\n".join(paginas)

        if not texto.strip():
            raise ValueError(
                f"'{path}' no tiene texto extraíble — probablemente es un PDF "
                "escaneado (solo imagen). Necesitas pasarlo por OCR antes de "
                "usarlo en este proyecto."
            )
        return texto

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_file(path: str, chunk_size: int = 200, overlap_sentences: int = 2) -> list[Chunk]:
    """Lee un .txt/.md/.pdf y lo parte en chunks. `source` = nombre del archivo."""
    text = extract_text(path)
    return chunk_text(
        text, source=os.path.basename(path), chunk_size=chunk_size, overlap_sentences=overlap_sentences
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python chunk.py ruta/al/archivo.txt")
        sys.exit(1)

    result = chunk_file(sys.argv[1])
    print(f"Total de chunks: {len(result)}\n")
    for c in result:
        print(f"--- chunk {c.index} ({len(c.text.split())} palabras) ---")
        print(c.text)
        print()