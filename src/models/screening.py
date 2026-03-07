from typing import List
from pydantic import BaseModel
from .query import Citation

class ScreeningRequest(BaseModel):
    modification_description: str

class CriteriaAnswer(BaseModel):
    question_number: int
    answer: str
    explanation: str

class ScreeningResponse(BaseModel):
    applicability_determination: str
    affected_design_functions: List[str]
    ufsar_cross_references: List[str]
    criteria_answers: List[CriteriaAnswer]
    additional_documents_to_review: List[str]
    citations: List[Citation]
    preliminary_warning: str = "PRELIMINARY DRAFT — NOT FOR REGULATORY SUBMISSION — REQUIRES LICENSED ENGINEER REVIEW"
