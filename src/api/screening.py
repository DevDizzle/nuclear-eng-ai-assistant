from fastapi import APIRouter
from src.models.screening import ScreeningRequest, ScreeningResponse
from src.agents.screening import ScreeningAgentWrapper

router = APIRouter()
agent = ScreeningAgentWrapper()

@router.post("/", response_model=ScreeningResponse)
async def generate_screening(request: ScreeningRequest):
    """Generates preliminary 50.59 screening draft."""
    return await agent.generate_screening(request)
