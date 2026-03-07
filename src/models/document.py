from typing import List, Optional
from pydantic import BaseModel, Field

class ChunkMetadata(BaseModel):
    document_id: str
    page_number: int
    section_header: Optional[str] = None
    chunk_index: int
    text: str

class DocumentCreate(BaseModel):
    filename: str
    content_type: str

class DocumentResponse(BaseModel):
    id: str
    filename: str
    upload_time: str
    status: str
    chunk_count: int
