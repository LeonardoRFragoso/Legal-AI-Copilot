from pypdf import PdfReader
from typing import List, Dict
import io


class PDFExtractor:
    @staticmethod
    def extract_text(file_bytes: bytes) -> tuple[str, int]:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text, len(reader.pages)
    
    @staticmethod
    def extract_text_by_page(file_bytes: bytes) -> List[Dict[str, any]]:
        reader = PdfReader(io.BytesIO(file_bytes))
        pages = []
        for i, page in enumerate(reader.pages):
            pages.append({
                "page_number": i + 1,
                "text": page.extract_text()
            })
        return pages
