from src.models.screening import ScreeningRequest, ScreeningResponse
from src.generation.gemini import GeminiClient
from src.generation.templates import SCREENING_SYSTEM_PROMPT

class ScreeningAgentWrapper:
    def __init__(self):
        self.llm = GeminiClient()

    async def generate_screening(self, request: ScreeningRequest) -> ScreeningResponse:
        prompt = f"Proposed Modification:\\n{request.modification_description}\\n\\nPlease generate a preliminary 50.59 screening."
        answer = await self.llm.generate_content(prompt, system_instruction=SCREENING_SYSTEM_PROMPT)
        
        return ScreeningResponse(
            applicability_determination=answer[:200] + "...",  # Simple placeholder for MVP demo
            affected_design_functions=["Feedwater flow control"],
            ufsar_cross_references=["Section 10.4.7"],
            criteria_answers=[],
            additional_documents_to_review=[],
            citations=[]
        )
