from typing import List, Optional
from pydantic import BaseModel, Field

class RetrievalHit(BaseModel):
    document_id: str
    filename: str
    title: Optional[str] = None
    doc_type: str
    plant_name: Optional[str] = None
    unit: Optional[str] = None
    revision: Optional[str] = None
    effective_date: Optional[str] = None
    section_id: Optional[str] = None
    section_header: Optional[str] = None
    page_number: int
    chunk_index: int
    source_uri: Optional[str] = None
    text: str
    distance: Optional[float] = None

class RetrievalRequest(BaseModel):
    query: str
    top_k: int = 10
    document_ids: Optional[List[str]] = None
    doc_types: Optional[List[str]] = None
    plant_name: Optional[str] = None
    unit: Optional[str] = None

class RetrievalResponse(BaseModel):
    hits: List[RetrievalHit]

    def format_for_llm(self) -> str:
        """Formats the retrieved hits into a compact context block for the LLM."""
        if not self.hits:
            return "No relevant documents found."
            
        context_parts = []
        for i, hit in enumerate(self.hits):
            meta = []
            if hit.filename: meta.append(f"File: {hit.filename}")
            if hit.doc_type: meta.append(f"Type: {hit.doc_type}")
            if hit.plant_name: meta.append(f"Plant: {hit.plant_name}")
            if hit.section_header: meta.append(f"Section: {hit.section_header}")
            if hit.page_number: meta.append(f"Page: {hit.page_number}")
            
            meta_str = " | ".join(meta)
            context_parts.append(f"--- Document {i+1} ({meta_str}) ---\n{hit.text}\n")
            
        return "\n".join(context_parts)
