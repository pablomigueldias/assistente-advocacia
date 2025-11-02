from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()

class Settings(BaseModel):
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3")
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "chroma_db")
    COLLECTION_NAME: str = os.getenv("COLLECTION_NAME", "docs_bpo")
    EMBEDDINGS_MODEL: str = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


settings = Settings()