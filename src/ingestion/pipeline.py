from src.storage.gcs import GCSStorage
from src.storage.firestore import FirestoreStorage
from src.ingestion.ocr import DocumentAIOCR
from src.ingestion.chunker import OverlappingChunker
from src.ingestion.embedder import VertexEmbedder
from src.models.document import DocumentCreate
import uuid

class IngestionPipeline:
    def __init__(self):
        self.gcs = GCSStorage()
        self.firestore = FirestoreStorage()
        self.ocr = DocumentAIOCR()
        self.chunker = OverlappingChunker()
        self.embedder = VertexEmbedder()

    async def process_document(self, file_path: str, doc_req: DocumentCreate) -> str:
        """Orchestrates the entire document ingestion process."""
        document_id = str(uuid.uuid4())
        
        # 1. Upload to GCS
        await self.gcs.upload_document(document_id, file_path)
        
        # 2. Extract Text
        text = await self.ocr.extract_text(file_path)
        
        # 3. Chunk Text
        chunks = self.chunker.chunk_text(
            document_id=document_id, 
            text=text,
            filename=doc_req.filename,
            doc_type=doc_req.doc_type,
            title=doc_req.title,
            plant_name=doc_req.plant_name,
            unit=doc_req.unit
        )
        
        # 4. Embed Chunks
        texts = [c.text for c in chunks]
        embeddings = await self.embedder.embed_chunks(texts)
        
        # 5. Store in Firestore
        metadata = {
            "id": document_id,
            "filename": doc_req.filename,
            "doc_type": doc_req.doc_type,
            "title": doc_req.title,
            "plant_name": doc_req.plant_name,
            "unit": doc_req.unit,
            "chunk_count": len(chunks),
            "status": "processed"
        }
        await self.firestore.store_document_metadata(document_id, metadata)
        await self.firestore.store_chunks(document_id, chunks, embeddings)
        
        return document_id
