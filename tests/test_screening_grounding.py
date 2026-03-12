import pytest
from src.adk.prompts.screening import SCREENING_INSTRUCTION

def test_screening_instruction_rules():
    assert "pre-retrieved plant-specific information" in SCREENING_INSTRUCTION
    assert "Do NOT hallucinate UFSAR sections" in SCREENING_INSTRUCTION
    assert "CONCRETE CITATIONS ONLY" in SCREENING_INSTRUCTION
    assert "FAIL CLOSED" in SCREENING_INSTRUCTION
    assert "You do not hold design authority" in SCREENING_INSTRUCTION
