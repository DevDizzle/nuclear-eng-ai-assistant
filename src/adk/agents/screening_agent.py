from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.callback_context import CallbackContext
from src.adk.prompts.screening import SCREENING_INSTRUCTION
from src.config import settings
from src.models.screening import ScreeningResponse
from src.retrieval.search import VectorSearch
from src.models.retrieval import RetrievalRequest

async def retrieve_screening_context(callback_context: CallbackContext, **kwargs):
    ctx = callback_context
    searcher = VectorSearch()
    # Find user message
    mod_desc = ""
    if ctx.session.events:
        for event in reversed(ctx.session.events):
            if event.author == "user":
                if event.content and event.content.parts:
                    mod_desc = event.content.parts[0].text
                break
    
    if not mod_desc:
        ctx.state["ufsar_context"] = "No modification description provided."
        ctx.state["guidance_context"] = "No modification description provided."
        return

    # 1. Retrieve UFSAR / Licensing Basis
    res_ufsar = await searcher.search(RetrievalRequest(query=mod_desc, top_k=5, doc_types=['ufsar', 'licensing_basis']))
    ctx.state["ufsar_context"] = res_ufsar.format_for_llm()
    
    # 2. Retrieve Guidance / Regulations
    res_guidance = await searcher.search(RetrievalRequest(query=mod_desc, top_k=5, doc_types=['regulation', 'regulatory_guide', 'industry_guidance']))
    ctx.state["guidance_context"] = res_guidance.format_for_llm()

def create_screening_researcher() -> Agent:
    instruction = SCREENING_INSTRUCTION + "\n\n=== RETRIEVED UFSAR CONTEXT ===\n{ufsar_context}\n\n=== RETRIEVED GUIDANCE CONTEXT ===\n{guidance_context}\n\nOutput a detailed research report including the applicability determination, affected functions, criteria answers, citations, and required documents."
    return Agent(
        name="screening_researcher",
        model=settings.llm_model,
        instruction=instruction,
        before_agent_callback=retrieve_screening_context,
        output_key="screening_draft"
    )

def create_screening_formatter() -> Agent:
    return Agent(
        name="screening_formatter",
        model=settings.llm_model_flash,
        instruction="Convert the following screening draft into the strictly required JSON structure representing the final screening: {screening_draft}",
        output_schema=ScreeningResponse,
        output_key="screening_result"
    )

def create_screening_pipeline() -> SequentialAgent:
    return SequentialAgent(
        name="screening_agent",
        description="Generates preliminary 10 CFR 50.59 screening drafts based on modification descriptions.",
        sub_agents=[create_screening_researcher(), create_screening_formatter()]
    )
