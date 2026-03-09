import json
from src.models.screening import ScreeningRequest, ScreeningResponse
from src.generation.gemini import GeminiClient
from src.generation.templates import SCREENING_SYSTEM_PROMPT

class ScreeningAgentWrapper:
    def __init__(self):
        self.llm = GeminiClient()

    async def generate_screening(self, request: ScreeningRequest) -> ScreeningResponse:
        prompt = f"""Proposed Modification:
{request.modification_description}

Please generate a preliminary 10 CFR 50.59 screening draft based on the modification description.
You MUST return your response as a valid JSON object with the following exact keys:
- "applicability_determination": A detailed string containing your assessment.
- "affected_design_functions": A list of strings representing the affected functions.
- "ufsar_cross_references": A list of strings representing potential UFSAR sections.

Do not include markdown formatting like ```json, just return the raw JSON object.
"""
        answer = await self.llm.generate_content(prompt, system_instruction=SCREENING_SYSTEM_PROMPT)
        
        try:
            # Clean up potential markdown formatting if the model still includes it
            cleaned_answer = answer.strip()
            if cleaned_answer.startswith("```json"):
                cleaned_answer = cleaned_answer[7:]
            if cleaned_answer.startswith("```"):
                cleaned_answer = cleaned_answer[3:]
            if cleaned_answer.endswith("```"):
                cleaned_answer = cleaned_answer[:-3]
                
            data = json.loads(cleaned_answer.strip())
            
            return ScreeningResponse(
                applicability_determination=data.get("applicability_determination", "Analysis generated but failed to parse correctly."),
                affected_design_functions=data.get("affected_design_functions", []),
                ufsar_cross_references=data.get("ufsar_cross_references", []),
                criteria_answers=[],
                additional_documents_to_review=[],
                citations=[]
            )
        except Exception as e:
            return ScreeningResponse(
                applicability_determination=f"Failed to parse LLM response into structured data. Raw output:\\n\\n{answer}\\n\\nError: {str(e)}",
                affected_design_functions=["Parsing Error"],
                ufsar_cross_references=["Parsing Error"],
                criteria_answers=[],
                additional_documents_to_review=[],
                citations=[]
            )
