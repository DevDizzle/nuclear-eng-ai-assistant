from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from src.agents.comparison import ComparisonAgent

class CompareRequest(BaseModel):
    spec_document_id: str
    vendor_document_ids: List[str]

class CompareResponse(BaseModel):
    comparison_table: str
    pass_fail_flags: dict

router = APIRouter()
agent = ComparisonAgent()

@router.post("/", response_model=CompareResponse)
async def compare_documents(request: CompareRequest):
    """Compares vendor bids against specifications."""
    return await agent.compare(request)
