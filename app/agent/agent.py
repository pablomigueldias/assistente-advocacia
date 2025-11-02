import re, json
from app.agent.schema import CATEGORIES, Extraction, AgentOutput
from app.agent.tools import tool_route, tool_checklist, tool_deadline_calc
from app.llm_client import chat as llm_chat

SYSTEM = (
    "Você é um agente de triagem de pedidos (BPO jurídico). "
    "Tarefas:\n"
    "1) Classificar o texto em: juridico, financeiro, rh, ti ou outros.\n"
    "2) Extrair campos (nome, email, data, assunto, sla_dias).\n"
    "3) Propor ações (rotear e checklist).\n"
    "Responda SEM rodeios, json puro em UTF-8 no formato:\n"
    '{"category": "...", "extraction": {...}}'
)

def classify_and_extract(texto: str):
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": f"Texto:\n{texto}\n\nResponda no formato pedido."}
    ]
    # usar a função importada llm_chat, sem temperature
    raw = llm_chat(messages)

    m = re.search(r"\{.*\}", raw, flags=re.S)
    if not m:
        raise ValueError("Modelo não retornou JSON válido:\n" + raw)

    data = json.loads(m.group(0))
    cat = (data.get("category") or "outros").lower()
    if cat not in CATEGORIES:
        cat = "outros"
    ext = Extraction(**(data.get("extraction") or {})).dict()
    return cat, ext

def agent_run(texto: str) -> AgentOutput:
    category, extraction = classify_and_extract(texto)
    route_res = tool_route(category, extraction)
    checklist = tool_checklist(category)

    actions = [route_res, checklist]

    sla = extraction.get("sla_dias")
    if sla is not None:
        try:
            actions.append(tool_deadline_calc(int(sla)))
        except Exception as e:
            actions.append({"action": "deadline_calc", "error": str(e)})

    return AgentOutput(
        category=category,
        extraction=Extraction(**extraction),
        actions=actions
    )
