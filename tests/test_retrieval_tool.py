import pytest
from src.models.retrieval import RetrievalRequest, RetrievalResponse, RetrievalHit

def test_retrieval_request_model():
    req = RetrievalRequest(query="test", top_k=5, doc_types=["ufsar"])
    assert req.query == "test"
    assert req.top_k == 5
    assert req.doc_types == ["ufsar"]

def test_retrieval_response_formatting():
    hit1 = RetrievalHit(
        document_id="1", filename="doc1.pdf", doc_type="ufsar", 
        plant_name="PlantA", page_number=5, chunk_index=0, text="Text chunk 1"
    )
    hit2 = RetrievalHit(
        document_id="2", filename="doc2.pdf", doc_type="regulation", 
        page_number=1, chunk_index=0, text="Text chunk 2"
    )
    
    res = RetrievalResponse(hits=[hit1, hit2])
    formatted = res.format_for_llm()
    
    assert "File: doc1.pdf" in formatted
    assert "Type: ufsar" in formatted
    assert "Plant: PlantA" in formatted
    assert "Text chunk 1" in formatted
    assert "Text chunk 2" in formatted
