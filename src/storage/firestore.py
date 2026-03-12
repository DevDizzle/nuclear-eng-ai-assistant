from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from src.config import settings
from src.models.document import ChunkMetadata
from typing import List, Dict, Any, Optional

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
        ops = 0
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            chunk_ref = self.db.collection("documents").document(document_id).collection("chunks").document(f"chunk_{i}")
            data = chunk.model_dump()
            data["embedding"] = Vector(embedding)
            batch.set(chunk_ref, data)
            ops += 1
            if ops >= 400:
                batch.commit()
                batch = self.db.batch()
                ops = 0
        if ops > 0:
            batch.commit()
        
    async def vector_search(
        self, 
        query_embedding: List[float], 
        top_k: int = 10, 
        document_ids: Optional[List[str]] = None, 
        doc_types: Optional[List[str]] = None, 
        plant_name: Optional[str] = None, 
        unit: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Performs vector search over chunks."""
        collection_group = self.db.collection_group("chunks")
        
        query = collection_group
        if document_ids:
            query = query.where(filter=firestore.FieldFilter("document_id", "in", document_ids[:30]))
            
        if doc_types:
            query = query.where(filter=firestore.FieldFilter("doc_type", "in", doc_types[:30]))
            
        if plant_name:
            query = query.where(filter=firestore.FieldFilter("plant_name", "==", plant_name))
            
        if unit:
            query = query.where(filter=firestore.FieldFilter("unit", "==", unit))

        vector_query = query.find_nearest(
            vector_field="embedding",
            query_vector=Vector(query_embedding),
            distance_measure=DistanceMeasure.COSINE,
            limit=top_k,
            distance_result_field="distance"
        )
        
        docs = vector_query.stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            if "embedding" in data:
                del data["embedding"]
            results.append(data)
            
        return results
        
    async def delete_document_data(self, document_id: str):
        """Deletes document and chunks from Firestore."""
        doc_ref = self.db.collection("documents").document(document_id)
        # Would need to delete subcollections first in a real implementation
        doc_ref.delete()
