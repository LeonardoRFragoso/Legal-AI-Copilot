from typing import List, Dict
import re


class Chunker:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, page_number: int = None) -> List[Dict[str, any]]:
        chunks = []
        
        # First, try to split by section headers (common in legal documents)
        # Look for patterns like "SECTION:", "CLAUSE:", or all-caps headers
        section_pattern = r'(?=\n[A-Z][A-Z\s]+\n)'
        sections = re.split(section_pattern, text)
        
        chunk_index = 0
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
            
            # If section is small enough, keep it as one chunk
            if len(section) <= self.chunk_size:
                chunks.append({
                    "chunk_index": chunk_index,
                    "text": section,
                    "page_number": page_number,
                    "chunk_metadata": {"token_count": len(section.split())}
                })
                chunk_index += 1
            else:
                # If section is too large, split by paragraphs
                paragraphs = re.split(r'\n\s*\n', section)
                
                current_chunk = ""
                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        continue
                    
                    if len(current_chunk) + len(para) <= self.chunk_size:
                        current_chunk += para + "\n\n"
                    else:
                        if current_chunk:
                            chunks.append({
                                "chunk_index": chunk_index,
                                "text": current_chunk.strip(),
                                "page_number": page_number,
                                "chunk_metadata": {"token_count": len(current_chunk.split())}
                            })
                            chunk_index += 1
                        
                        # If paragraph is larger than chunk_size, split it by words
                        if len(para) > self.chunk_size:
                            words = para.split()
                            for i in range(0, len(words), self.chunk_size):
                                chunk_text = " ".join(words[i:i + self.chunk_size])
                                chunks.append({
                                    "chunk_index": chunk_index,
                                    "text": chunk_text,
                                    "page_number": page_number,
                                    "chunk_metadata": {"token_count": len(chunk_text.split())}
                                })
                                chunk_index += 1
                            current_chunk = ""
                        else:
                            current_chunk = para + "\n\n"
                
                if current_chunk:
                    chunks.append({
                        "chunk_index": chunk_index,
                        "text": current_chunk.strip(),
                        "page_number": page_number,
                        "chunk_metadata": {"token_count": len(current_chunk.split())}
                    })
                    chunk_index += 1
        
        # If no chunks were created, fall back to simple splitting
        if not chunks:
            paragraphs = re.split(r'\n\s*\n', text)
            for para in paragraphs:
                para = para.strip()
                if para:
                    chunks.append({
                        "chunk_index": len(chunks),
                        "text": para,
                        "page_number": page_number,
                        "chunk_metadata": {"token_count": len(para.split())}
                    })
        
        return chunks
