from google.adk.tools import ToolContext
from src.retrieval.search import VectorSearch
from src.models.retrieval import RetrievalRequest
from typing import List, Optional

async def search_documents(
    query: str,
    top_k: int = 10,
    doc_types: Optional[List[str]] = None,
    plant_name: Optional[str] = None,
    unit: Optional[str] = None,
    tool_context: Optional[ToolContext] = None
) -> dict:
    """Searches the vector database for relevant documents to ground the answer.

    Args:
        query: The search query string.
        top_k: The number of top results to return.
        doc_types: Optional list of document types to filter by (e.g. ['ufsar', 'regulation']).
        plant_name: Optional plant name to filter by.
        unit: Optional unit to filter by.

    Returns:
        dict with 'status' and 'context' keys containing the formatted retrieval text.
    """
    search_service = VectorSearch()
    
    req = RetrievalRequest(
        query=query,
        top_k=top_k,
        doc_types=doc_types,
        plant_name=plant_name,
        unit=unit
    )
    
    response = await search_service.search(req)
    
    return {
        "status": "success",
        "context": response.format_for_llm(),
        "hit_count": len(response.hits)
    }
