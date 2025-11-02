import ollama
from app.config import settings


SYSTEM_DEFAULT = """
Você é um assistente técnico, direto e didático. Responda em PT-BR e cite passos claros quando for útil.
""".strip()




def chat(messages, model: str | None = None):
    model = model or settings.LLM_MODEL
    return ollama.chat(model=model, messages=messages)["message"]["content"]




def simple_answer(prompt: str, system: str | None = None, model: str | None = None) -> str:
    system = system or SYSTEM_DEFAULT
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    return chat(msgs, model=model)