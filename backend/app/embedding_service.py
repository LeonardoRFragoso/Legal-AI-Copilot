from langchain_openai import OpenAIEmbeddings
from app.config import get_settings
import os

settings = get_settings()


class EmbeddingService:
    def __init__(self):
        api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. Embedding service will not work.")
            self.embeddings = None
        else:
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                openai_api_key=api_key
            )
    
    def generate_embedding(self, text: str) -> list:
        if not self.embeddings:
            raise ValueError("OPENAI_API_KEY not configured")
        return self.embeddings.embed_query(text)
    
    def generate_embeddings_batch(self, texts: list[str]) -> list[list]:
        if not self.embeddings:
            raise ValueError("OPENAI_API_KEY not configured")
        return self.embeddings.embed_documents(texts)
