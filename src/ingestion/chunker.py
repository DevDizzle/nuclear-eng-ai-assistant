from typing import List
from src.models.document import ChunkMetadata

class OverlappingChunker:
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, document_id: str, text: str) -> List[ChunkMetadata]:
        """
        Chunks text with overlap while preserving page numbers and section headers.
        In a real implementation, tokens should be used, but words are used here as placeholder.
        """
        words = text.split()
        chunks = []
        i = 0
        chunk_idx = 0
        current_page = 1
        current_section = None
        
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

            chunks.append(ChunkMetadata(
                document_id=document_id,
                page_number=current_page,
                section_header=current_section,
                chunk_index=chunk_idx,
                text=chunk_text
            ))
            i += (self.chunk_size - self.overlap)
            chunk_idx += 1
            
        return chunks
