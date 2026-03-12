from typing import List, Optional
from src.models.document import ChunkMetadata
import re

class OverlappingChunker:
    """
    WARNING: This is a naive overlapping word chunker with simple regex heuristics 
    for page and section tracking. It is sufficient for a demo but NOT recommended 
    for production regulatory documents.
    
    Next Upgrade Path: Replace this with a layout-aware parser (e.g., LlamaParse, 
    Docling, or Unstructured) to reliably extract true semantic sections, tables, 
    and document hierarchies from complex PDFs like UFSARs and SERs.
    """
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, document_id: str, text: str, filename: str, doc_type: str = "other", title: Optional[str] = None, plant_name: Optional[str] = None, unit: Optional[str] = None) -> List[ChunkMetadata]:
        """
        Chunks text with overlap while preserving page numbers and section headers.
        """
        words = text.split()
        chunks = []
        i = 0
        chunk_idx = 0
        current_page = 1
        current_section_header = None
        current_section_id = None
        
        while i < len(words):
            chunk_words = words[i:i+self.chunk_size]
            chunk_text = " ".join(chunk_words)
            
            # Simple heuristic for page tracking
            if "[PAGE_" in chunk_text:
                parts = chunk_text.split("[PAGE_")
                if len(parts) > 1 and "]" in parts[1]:
                    try:
                        current_page = int(parts[1].split("]")[0])
                    except ValueError:
                        pass
            
            # Simple heuristic for section tracking
            lines = chunk_text.split('\n')
            for line in lines:
                if re.match(r'^\d+\.\d+(\.\d+)*\s+[A-Z]', line):
                    parts = line.split(maxsplit=1)
                    if len(parts) > 1:
                        current_section_id = parts[0]
                        current_section_header = parts[1][:100] # truncate

            chunks.append(ChunkMetadata(
                document_id=document_id,
                filename=filename,
                title=title,
                doc_type=doc_type,
                plant_name=plant_name,
                unit=unit,
                page_number=current_page,
                section_id=current_section_id,
                section_header=current_section_header,
                chunk_index=chunk_idx,
                text=chunk_text
            ))
            i += (self.chunk_size - self.overlap)
            chunk_idx += 1
            
        return chunks
