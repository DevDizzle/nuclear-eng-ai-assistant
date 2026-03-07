from fastapi import APIRouter
from src.models.audit import AuditEntry
from typing import List

router = APIRouter()

@router.post("/", response_model=List[AuditEntry])
async def query_audit_log():
    """Queries the audit log."""
    return []
