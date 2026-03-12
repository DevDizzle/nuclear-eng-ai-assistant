from typing import List, Dict, Any, Optional
from src.storage.firestore import FirestoreStorage
from src.ingestion.embedder import VertexEmbedder
from src.models.retrieval import RetrievalRequest, RetrievalResponse, RetrievalHit

class VectorSearch:
    def __init__(self):
        self.firestore = FirestoreStorage()
        self.embedder = VertexEmbedder()

    async def search(self, request: RetrievalRequest) -> RetrievalResponse:
        """Embeds query and performs vector search in Firestore."""
        query_embeddings = await self.embedder.embed_chunks([request.query])
        query_embedding = query_embeddings[0]
        
        results = await self.firestore.vector_search(
            query_embedding=query_embedding, 
            top_k=request.top_k, 
            document_ids=request.document_ids,
            doc_types=request.doc_types,
            plant_name=request.plant_name,
            unit=request.unit
        )
        
        hits = []
        for res in results:
            # handle backwards compatibility if old data is lacking fields
            hits.append(RetrievalHit(
                document_id=res.get("document_id", "unknown"),
                filename=res.get("filename", "unknown"),
                title=res.get("title"),
                doc_type=res.get("doc_type", "other"),
                plant_name=res.get("plant_name"),
                unit=res.get("unit"),
                revision=res.get("revision"),
                effective_date=res.get("effective_date"),
                section_id=res.get("section_id"),
                section_header=res.get("section_header"),
                page_number=res.get("page_number", 0),
                chunk_index=res.get("chunk_index", 0),
                source_uri=res.get("source_uri"),
                text=res.get("text", ""),
                distance=res.get("distance")
            ))
            
        return RetrievalResponse(hits=hits)
