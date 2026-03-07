from typing import List, Dict, Any
from src.storage.firestore import FirestoreStorage
from src.ingestion.embedder import VertexEmbedder

class VectorSearch:
    def __init__(self):
        self.firestore = FirestoreStorage()
        self.embedder = VertexEmbedder()

    async def search(self, query: str, top_k: int = 10, document_ids: List[str] = None) -> List[Dict[str, Any]]:
        """Embeds query and performs vector search in Firestore."""
        query_embeddings = await self.embedder.embed_chunks([query])
        query_embedding = query_embeddings[0]
        
        results = await self.firestore.vector_search(query_embedding, top_k, document_ids)
        return results
