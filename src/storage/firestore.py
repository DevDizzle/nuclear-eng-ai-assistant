from google.cloud import firestore
from src.config import settings
from src.models.document import ChunkMetadata
from typing import List, Dict, Any

class FirestoreStorage:
    def __init__(self):
        self.db = firestore.Client(project=settings.gcp_project_id, database=settings.firestore_database)

    async def store_document_metadata(self, document_id: str, metadata: dict):
        """Stores document metadata in Firestore."""
        doc_ref = self.db.collection("documents").document(document_id)
        doc_ref.set(metadata)

    async def store_chunks(self, document_id: str, chunks: List[ChunkMetadata], embeddings: List[List[float]]):
        """Stores document chunks and embeddings."""
        batch = self.db.batch()
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_ref = self.db.collection("documents").document(document_id).collection("chunks").document(f"chunk_{i}")
            data = chunk.model_dump()
            data["embedding"] = embedding
            batch.set(chunk_ref, data)
        batch.commit()
        
    async def vector_search(self, query_embedding: List[float], top_k: int = 10, document_ids: List[str] = None) -> List[Dict[str, Any]]:
        """Performs vector search over chunks. 
        Note: This is a placeholder for actual Firestore vector search implementation.
        """
        # In a real implementation, use vector search query on Firestore.
        return []
        
    async def delete_document_data(self, document_id: str):
        """Deletes document and chunks from Firestore."""
        doc_ref = self.db.collection("documents").document(document_id)
        # Would need to delete subcollections first
        doc_ref.delete()
