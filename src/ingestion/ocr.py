from typing import List
import PyPDF2

class DocumentAIOCR:
    def __init__(self):
        # Initialize Google Document AI client
        pass

    async def extract_text(self, file_path: str) -> str:
        """Extract text from PDF preserving page numbers. Uses PyPDF2 for native PDFs."""
        text = ""
        if file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            return text
            
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                # Include page marker for chunking context
                text += f"\n[PAGE_{i+1}]\n{page_text}"
        return text
