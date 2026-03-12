from fastapi import APIRouter, HTTPException
from src.models.query import QueryRequest, QueryResponse
from src.adk.agents.retrieval_agent import create_retrieval_pipeline
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid

router = APIRouter()
# Use a single session service for the app
session_service = InMemorySessionService()
agent = create_retrieval_pipeline()

@router.post("/", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """RAG Q&A endpoint using ADK."""
    session_id = str(uuid.uuid4())
    user_id = "default_user"
    
    await session_service.create_session(
        app_name="nuclear_assistant", 
        user_id=user_id, 
        session_id=session_id
    )
    
    runner = Runner(
        agent=agent, 
        app_name="nuclear_assistant", 
        session_service=session_service
    )
    
    # Run the pipeline
    async for _ in runner.run_async(
        user_id=user_id, 
        session_id=session_id,
        new_message=types.Content(role="user", parts=[types.Part.from_text(text=request.question)])
    ):
        pass
        
    # Get the final state
    session = await session_service.get_session(
        app_name="nuclear_assistant", 
        user_id=user_id, 
        session_id=session_id
    )
    
    result = session.state.get("retrieval_result")
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate retrieval result.")
        
    return result
