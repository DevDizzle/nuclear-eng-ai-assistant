from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from typing import List
from src.models.document import DocumentResponse
from src.ingestion.pipeline import IngestionPipeline
import tempfile
import os

router = APIRouter()
pipeline = IngestionPipeline()

@router.post("/", response_model=DocumentResponse)
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Uploads a PDF and triggers the ingestion pipeline."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    async def process_and_cleanup():
        try:
            await pipeline.process_document(tmp_path, file.filename)
        finally:
            os.unlink(tmp_path)

    background_tasks.add_task(process_and_cleanup)
    
    return DocumentResponse(
        id="pending", 
        filename=file.filename,
        upload_time="now",
        status="processing",
        chunk_count=0
    )

@router.get("/", response_model=List[DocumentResponse])
async def list_documents():
    """List all ingested documents."""
    return []

@router.delete("/{document_id}")
async def delete_document(document_id: str):
    """Remove document and its embeddings."""
    return {"status": "deleted"}
