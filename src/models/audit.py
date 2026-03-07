from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class AuditEntry(BaseModel):
    timestamp: datetime
    user_id: str
    action: str
    endpoint: str
    query_text: Optional[str] = None
    referenced_documents: List[str]
    generated_citations: int
    response_status: int
