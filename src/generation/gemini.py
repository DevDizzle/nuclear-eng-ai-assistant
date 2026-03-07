import google.genai as genai
from google.genai import types
from src.config import settings

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(
            vertexai=True,
            project=settings.gcp_project_id,
            location=settings.gcp_region
        )
        self.model = settings.llm_model

    async def generate_content(self, prompt: str, system_instruction: str = None) -> str:
        """Generates content using Gemini."""
        config = types.GenerateContentConfig()
        if system_instruction:
            config.system_instruction = system_instruction
            
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config
        )
        return response.text
