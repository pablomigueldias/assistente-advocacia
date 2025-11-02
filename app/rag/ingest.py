import os
import re
import pathlib
from typing import List, Tuple
from pypdf import PdfReader

from app.rag.splitter import chunk_text
from app.rag.vectorstore import VectorStore

DATA_DIR = pathlib.Path("data/docs")

def clean_text_for_rag(text: str) -> str:
    text = re.sub(r'[_]{3,}', ' {{LACUNA}} ', text)
    text = re.sub(r'[-]{3,}', ' {{LACUNA}} ', text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    return text

def load_docs_recursive(folder: pathlib.Path) -> List[Tuple[str, str]]:
    
    docs = []

    for path in folder.rglob("*.pdf"):
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        full = "\n".join(pages).strip()
        if full:
            rel = str(path.relative_to(folder)).replace("\\", "/")
            docs.append((rel, full))
        else:
            print(f"[RAG] Aviso: '{path.name}' sem texto (OCR seria necessário).")

    for path in folder.rglob("*.txt"):
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            rel = str(path.relative_to(folder)).replace("\\", "/")
            docs.append((rel, text))

    return docs

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    vs = VectorStore()
    try:
        vs.reset()
    except Exception as e:
        print(f"[RAG] Aviso ao resetar coleção: {e}")

    loaded = load_docs_recursive(DATA_DIR)
    if not loaded:
        print(f"[RAG] Nenhum documento encontrado em {DATA_DIR} (pdf ou txt).")
        return

    for fname, raw_text in loaded:
        text = clean_text_for_rag(raw_text)
        file_is_template = "{{LACUNA}}" in text

        chunks = chunk_text(text)

        metas = []
        for i, ch in enumerate(chunks):
            chunk_is_template = file_is_template or ("{{LACUNA}}" in ch)
            metas.append({
                "source": fname,
                "chunk": i,
                "type": "template" if chunk_is_template else "documento"
            })

        ids = [f"{fname}_{i}" for i in range(len(chunks))]
        vs.add(chunks, metas, ids)

    print("[RAG] Ingestão concluída.")

if __name__ == "__main__":
    main()
