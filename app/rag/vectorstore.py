import chromadb
from chromadb.config import Settings
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
from app.config import settings

class VectorStore:
    def __init__(self):
        
        self.client = chromadb.PersistentClient(
            path=settings.CHROMA_DIR,
            settings=Settings()
        )
        self.collection_name = settings.COLLECTION_NAME

        try:
            self.col = self.client.get_collection(self.collection_name)
        except Exception:
            self.col = self.client.create_collection(self.collection_name)

       
        self.embedder = SentenceTransformer(settings.EMBEDDINGS_MODEL)

    def reset(self):
       
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.col = self.client.create_collection(self.collection_name)

    def add(self, documents: List[str], metadatas: List[Dict], ids: List[str]):
        
        embs = self.embedder.encode(
            documents, batch_size=32, convert_to_numpy=True
        ).tolist()
        self.col.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embs
        )

    def query(self, query: str, k: int = 4) -> List[Tuple[str, Dict]]:
       
        q_emb = self.embedder.encode([query], convert_to_numpy=True)[0].tolist()
        res = self.col.query(query_embeddings=[q_emb], n_results=k)
        docs = res["documents"][0]
        metas = res["metadatas"][0]
        return list(zip(docs, metas))
