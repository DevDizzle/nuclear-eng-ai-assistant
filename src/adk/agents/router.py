from google.adk.agents import Agent
from src.adk.prompts.router import ROUTER_INSTRUCTION
from src.adk.agents.retrieval_agent import create_retrieval_pipeline
from src.adk.agents.screening_agent import create_screening_pipeline
from src.config import settings

def create_router_agent() -> Agent:
    return Agent(
        name="router_agent",
        model=settings.llm_model_flash,
        instruction=ROUTER_INSTRUCTION,
        sub_agents=[create_retrieval_pipeline(), create_screening_pipeline()]
    )
