from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm_client import simple_answer
from app.rag.query import answer_query
from app.agent.agent import agent_run



app = FastAPI(title="Chat Jurídico IA Demo")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatIn(BaseModel):
    message: str


@app.post("/chat")
def chat(inp: ChatIn):
    return {"answer": simple_answer(inp.message)}


class RagIn(BaseModel):
    query: str


@app.post("/rag/query")
def rag(inp: RagIn):
    return {"answer": answer_query(inp.query)}

@app.post("/rag/peek")
def rag_peek(inp: RagIn):
    return {"hits": peek_hits(inp.query, k=5)}


class AgentIn(BaseModel):
    text: str


@app.post("/agent/route")
def agent_endpoint(inp: AgentIn):
    out = agent_run(inp.text)
    return out.model_dump()

