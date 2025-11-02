from datetime import datetime, timedelta
from app.agent.schema import CATEGORIES

def tool_route(category: str, payload: dict):
    category = category if category in CATEGORIES else "outros"
    return {
        "action": "route",
        "category": category,
        "queue": f"fila_{category}",
        "payload": payload,
        "note": "Roteado com sucesso."
    }

def tool_checklist(category: str):
    check = {
        "juridico": ["Verificar procuração", "Conferir cláusula de multa", "Revisar confidencialidade/LGPD", "Gerar minuta/aditivo"],
        "financeiro": ["Conferir NF", "Validar pagamento", "Atualizar planilha"],
        "rh": ["Checar cadastro", "Solicitar documentos", "Agendar entrevista"],
        "ti": ["Reproduzir erro", "Checar logs", "Abrir tarefa"],
        "outros": ["Entender demanda", "Designar responsável", "Definir prazo"],
    }
    return {"action": "checklist", "items": check.get(category, check["outros"])}

def tool_deadline_calc(sla_dias: int):
    if not isinstance(sla_dias, int) or sla_dias <= 0:
        return {"action": "deadline_calc", "error": "sla_dias inválido"}
    dt = (datetime.now() + timedelta(days=sla_dias)).strftime("%d/%m/%Y")
    return {"action": "deadline_calc", "deadline_corridos": dt}
