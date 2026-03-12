from fastapi import APIRouter, HTTPException
from src.models.screening import ScreeningRequest, ScreeningResponse
from src.adk.agents.screening_agent import create_screening_pipeline
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import uuid

router = APIRouter()
session_service = InMemorySessionService()
agent = create_screening_pipeline()

@router.post("", response_model=ScreeningResponse)
async def generate_screening(request: ScreeningRequest):
    """Generates preliminary 50.59 screening draft using ADK."""
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
    prompt = f"Proposed Modification:\n{request.modification_description}\n\nPlease generate a 10 CFR 50.59 screening."
    async for _ in runner.run_async(
        user_id=user_id, 
        session_id=session_id,
        new_message=types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    ):
        pass
        
    # Get the final state
    session = await session_service.get_session(
        app_name="nuclear_assistant", 
        user_id=user_id, 
        session_id=session_id
    )
    
    result = session.state.get("screening_result")
    if not result:
        raise HTTPException(status_code=500, detail="Failed to generate screening result.")
        
    return result
