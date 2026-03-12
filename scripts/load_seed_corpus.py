import asyncio
import os
from src.ingestion.pipeline import IngestionPipeline
from src.models.document import DocumentCreate

async def load_seed_corpus():
    pipeline = IngestionPipeline()
    seed_docs = [
        {"path": "data/sample_documents/NEI_96_07.pdf", "doc_type": "industry_guidance", "title": "NEI 96-07 Rev 1"},
        {"path": "data/sample_documents/St_Lucie_Unit1_SER.pdf", "doc_type": "other", "title": "St. Lucie Unit 1 SER"},
        {"path": "data/sample_documents/Turkey_Point_EPU_Report.pdf", "doc_type": "licensing_basis", "title": "Turkey Point EPU Report", "plant_name": "Turkey Point"},
        {"path": "data/sample_documents/Turkey_Point_LAR_280_Fire_Protection.pdf", "doc_type": "licensing_basis", "title": "Turkey Point LAR 280", "plant_name": "Turkey Point"},
        {"path": "data/sample_documents/Turkey_Point_UFSAR_Main_Steam.txt", "doc_type": "ufsar", "title": "Turkey Point UFSAR Chapters 10, 11, 14", "plant_name": "Turkey Point"},
    ]
    
    for doc in seed_docs:
        if os.path.exists(doc["path"]):
            print(f"Ingesting {doc['path']}...")
            req = DocumentCreate(
                filename=os.path.basename(doc["path"]),
                content_type="application/pdf",
                doc_type=doc["doc_type"],
                title=doc["title"],
                plant_name=doc.get("plant_name")
            )
            doc_id = await pipeline.process_document(doc["path"], req)
            print(f"Success! Document ID: {doc_id}")
        else:
            print(f"File not found: {doc['path']}")

if __name__ == "__main__":
    asyncio.run(load_seed_corpus())
