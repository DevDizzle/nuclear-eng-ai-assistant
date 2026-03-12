# DEPRECATED: This wrapper is replaced by src/adk/agents/retrieval_agent.py
from src.retrieval.search import VectorSearch
from src.retrieval.reranker import Reranker
from src.generation.gemini import GeminiClient
from src.generation.citations import CitationExtractor
from src.generation.templates import QA_SYSTEM_PROMPT
from src.models.query import QueryRequest, QueryResponse

class RetrievalAgentWrapper:
    def __init__(self):
        self.search_tool = VectorSearch()
        self.reranker = Reranker()
        self.llm = GeminiClient()
        self.citation_extractor = CitationExtractor()
        
    async def run_query(self, request: QueryRequest) -> QueryResponse:
        results = await self.search_tool.search(request.question, top_k=5)
        context = "\\n\\n".join([r.get("text", "") for r in results])
        
        prompt = f"Context:\\n{context}\\n\\nQuestion:\\n{request.question}"
        answer = await self.llm.generate_content(prompt, system_instruction=QA_SYSTEM_PROMPT)
        
        citations = self.citation_extractor.extract(answer, results)
        return QueryResponse(answer=answer, citations=citations)
