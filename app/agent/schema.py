from pydantic import BaseModel, Field
from typing import Optional, List

CATEGORIES = ["juridico", "financeiro", "rh", "ti", "outros"]

class Extraction(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    data: Optional[str] = None
    assunto: Optional[str] = None
    sla_dias: Optional[int] = Field(default=None, description="SLA em dias inteiros")

class AgentOutput(BaseModel):
    category: str
    extraction: Extraction
    actions: List[dict]
