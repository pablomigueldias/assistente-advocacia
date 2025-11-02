import sys
from app.llm_client import chat


SYSTEM_PROMPT = """
Você é um assistente técnico, direto e didático.
Responda em PT-BR. Seja claro e objetivo.
""".strip()




def chat_loop(model=None):
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Chat Llama 3 (digite 'sair' para encerrar)")
    while True:
        user = input("Você: ").strip()
        if user.lower() in ("sair", "exit", "quit"):
        print("Tchau!")
        break
    history.append({"role": "user", "content": user})
    answer = chat(history, model=model)
    print("\nAssistente:", answer, "\n")
    history.append({"role": "assistant", "content": answer})


    if __name__ == "__main__":
        model = sys.argv[1] if len(sys.argv) > 1 else None
        chat_loop(model)