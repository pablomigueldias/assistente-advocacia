# app/rag/query.py
from typing import List, Tuple, Dict
from app.rag.vectorstore import VectorStore
from app.llm_client import chat as llm_chat

SYSTEM_RAG = (
    "Você é um assistente jurídico. Responda em PT-BR, de forma objetiva e fiel ao CONTEXTO abaixo.\n"
    "Se existir {{LACUNA}} (antigas linhas em branco), não invente conteúdo: explique que é um campo a ser preenchido.\n"
    "Se o contexto não cobrir a pergunta, diga isso explicitamente. Sempre finalize com: 'Fontes: nome_arquivo_1; nome_arquivo_2'."
)

def peek_hits(question: str, k: int = 5) -> List[Dict]:
   
    vs = VectorStore()
    hits: List[Tuple[str, Dict]] = vs.query(question, k=k)
    out = []
    for doc, meta in hits:
        out.append({
            "source": meta.get("source"),
            "type": meta.get("type"),
            "chunk": meta.get("chunk"),
            "preview": (doc[:280] + "…") if len(doc) > 280 else doc
        })
    return out

def _format_context(hits: List[Tuple[str, Dict]]) -> str:

    parts = []
    for doc, meta in hits:
        src = meta.get("source", "desconhecido")
        parts.append(f"[{src}] {doc}")
    return "\n\n".join(parts)

def _format_sources(hits: List[Tuple[str, Dict]]) -> str:
    seen = []
    for _, meta in hits:
        s = meta.get("source", "desconhecido")
        if s not in seen:
            seen.append(s)
    return "; ".join(seen)

def _prioritize(hits: List[Tuple[str, Dict]]) -> List[Tuple[str, Dict]]:
   
    def score(meta):
        t = (meta or {}).get("type", "documento")
        return 0 if t == "documento" else 1
    return sorted(hits, key=lambda x: score(x[1]))

def answer_query(question: str, k: int = 4) -> str:
    vs = VectorStore()
    
    hits: List[Tuple[str, Dict]] = vs.query(question, k=k)

    if not hits:
        return "Não encontrei conteúdo suficiente nos documentos para responder com segurança.\n\nFontes: "

    hits = _prioritize(hits)

    ctx = _format_context(hits)
    fontes = _format_sources(hits)

    messages = [
        {"role": "system", "content": SYSTEM_RAG},
        {"role": "user", "content": f"Pergunta: {question}\n\nCONTEXT0:\n{ctx}\n\nResponda com base APENAS no CONTEXTO."}
    ]
    answer = llm_chat(messages).strip()
   
    if "Fontes:" not in answer:
        answer = f"{answer}\n\nFontes: {fontes}"
    return answer
