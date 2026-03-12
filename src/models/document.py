from typing import List, Optional
from pydantic import BaseModel, Field

class ChunkMetadata(BaseModel):
    document_id: str
    filename: str
    title: Optional[str] = None
    doc_type: str = "other"  # regulation, regulatory_guide, industry_guidance, ufsar, procedure, design_basis, licensing_basis, other
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

class DocumentCreate(BaseModel):
    filename: str
    content_type: str
    doc_type: str = "other"
    title: Optional[str] = None
    plant_name: Optional[str] = None
    unit: Optional[str] = None

class DocumentResponse(BaseModel):
    id: str
    filename: str
    upload_time: str
    status: str
    chunk_count: int
