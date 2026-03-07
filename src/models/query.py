from typing import List, Optional
from pydantic import BaseModel

class Citation(BaseModel):
    source_document: str
    page_number: int
    relevant_passage: str
    confidence: str

class QueryRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
    preliminary_warning: str = "⚠️ PRELIMINARY — AI-GENERATED CONTENT — REQUIRES LICENSED ENGINEER REVIEW AND APPROVAL"
