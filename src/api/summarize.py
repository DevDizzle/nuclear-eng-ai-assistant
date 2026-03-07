from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.summarization import SummarizationAgent

class SummarizeRequest(BaseModel):
    document_id: str

class SummarizeResponse(BaseModel):
    executive_summary: str
    section_breakdown: list

router = APIRouter()
agent = SummarizationAgent()

@router.post("/", response_model=SummarizeResponse)
async def summarize_document(request: SummarizeRequest):
    """Generates an executive summary of a document."""
    return await agent.summarize(request)
