.PHONY: setup pull ingest api chat


setup:
python -m venv .venv && . .venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt


pull:
ollama pull llama3 || true


ingest:
python -m app.rag.ingest


api:
uvicorn app.api.main:app --reload


chat:
python scripts/chat_cli.py