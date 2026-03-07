from fastapi import APIRouter
from src.models.query import QueryRequest, QueryResponse
from src.agents.retrieval import RetrievalAgentWrapper

router = APIRouter()
agent = RetrievalAgentWrapper()

@router.post("/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """RAG Q&A endpoint."""
    return await agent.run_query(request)
