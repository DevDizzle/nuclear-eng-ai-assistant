from google.adk.agents import Agent, SequentialAgent
from src.adk.prompts.retrieval import RETRIEVAL_INSTRUCTION
from src.adk.tools.vector_retrieval import search_documents
from src.config import settings
from src.models.query import QueryResponse

def create_retrieval_researcher() -> Agent:
    return Agent(
        name="retrieval_researcher",
        model=settings.llm_model_flash,
        instruction=RETRIEVAL_INSTRUCTION + "\n\nUse the search_documents tool to answer the user's question. Write a detailed response with clear citations to the source documents.",
        tools=[search_documents],
        output_key="retrieval_draft"
    )

def create_retrieval_formatter() -> Agent:
    return Agent(
        name="retrieval_formatter",
        model=settings.llm_model_flash,
        instruction="Convert the following research draft into the strictly required JSON structure representing the final answer with citations: {retrieval_draft}",
        output_schema=QueryResponse,
        output_key="retrieval_result"
    )

def create_retrieval_pipeline() -> SequentialAgent:
    return SequentialAgent(
        name="retrieval_agent",
        description="Retrieves information from plant documents, regulations, and industry guidance to answer technical questions.",
        sub_agents=[create_retrieval_researcher(), create_retrieval_formatter()]
    )
