"""
RAG Service - Unified Retrieval, Context Building, and Citation Management.

Provides a single, deterministic RAG pipeline that:
1. Retrieves chunks once per query
2. Builds context from those chunks
3. Constructs citations from those chunks
4. Validates using the same chunks

This ensures that the LLM and validator use the exact same evidence.
"""

from dataclasses import dataclass
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models import Document, Chunk, DocumentEmbedding
from app.config import get_settings
from app.logger import logger
import numpy as np
import pickle

settings = get_settings()


class RAGProviderUnavailableError(Exception):
    """Raised when the embedding provider is unavailable (e.g., API key invalid, timeout)."""
    pass


class RAGRetrievalError(Exception):
    """Raised when retrieval fails for other reasons (e.g., database error)."""
    pass


@dataclass
class RetrievedChunk:
    """Represents a single chunk retrieved from the RAG pipeline."""
    chunk_id: str
    document_id: str
    document_title: str
    page_number: Optional[int]
    text: str
    similarity_score: float

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "chunk_id": self.chunk_id,
            "document_id": self.document_id,
            "document_title": self.document_title,
            "page_number": self.page_number,
            "text": self.text,
            "similarity_score": self.similarity_score,
        }


class RAGService:
    """Unified RAG service for retrieval, context building, and citations."""

    # Configuration
    TOP_K = 5
    MIN_SIMILARITY_SCORE = 0.3

    def __init__(self, db: Session):
        """Initialize RAG service with database session."""
        self.db = db
        self.top_k = int(settings.rag_top_k) if hasattr(settings, 'rag_top_k') else self.TOP_K
        self.min_similarity = float(settings.min_similarity_score) if hasattr(settings, 'min_similarity_score') else self.MIN_SIMILARITY_SCORE

    def retrieve(self, query: str, document_id: Optional[str] = None) -> List[RetrievedChunk]:
        """
        Retrieve chunks using semantic search.

        Args:
            query: The search query
            document_id: Optional document ID to limit search scope

        Returns:
            List of RetrievedChunk objects sorted by similarity (descending)
            
        Raises:
            RAGProviderUnavailableError: If embedding provider is unavailable (API key, timeout, etc.)
            RAGRetrievalError: If retrieval fails for other reasons (database error, etc.)
        """
        try:
            from app.embedding_service import EmbeddingService
            embedding_service = EmbeddingService()

            # Generate query embedding
            try:
                query_embedding = embedding_service.generate_embedding(query)
            except Exception as e:
                # Check if it's an authentication or provider error
                error_str = str(e).lower()
                if "api" in error_str or "authentication" in error_str or "401" in error_str or "timeout" in error_str:
                    logger.error(f"RAG provider unavailable: {str(e)}")
                    raise RAGProviderUnavailableError(f"Embedding provider unavailable: {str(e)}")
                else:
                    raise

            # Retrieve embeddings from database
            try:
                embeddings_query = self.db.query(DocumentEmbedding)

                if document_id:
                    embeddings_query = embeddings_query.filter(DocumentEmbedding.document_id == document_id)

                embeddings = embeddings_query.all()
            except Exception as e:
                logger.error(f"Database retrieval failed: {str(e)}")
                raise RAGRetrievalError(f"Database retrieval failed: {str(e)}")

            results = []
            for emb in embeddings:
                if emb.embedding:
                    try:
                        stored_embedding = pickle.loads(emb.embedding)
                    except Exception:
                        continue

                    similarity = self._cosine_similarity(query_embedding, stored_embedding)

                    # Apply threshold
                    if similarity >= self.min_similarity:
                        results.append(
                            RetrievedChunk(
                                chunk_id=emb.chunk_id,
                                document_id=emb.chunk.document.id,
                                document_title=emb.chunk.document.title,
                                page_number=emb.chunk.page_number,
                                text=emb.chunk.text,
                                similarity_score=float(similarity),
                            )
                        )

            # Sort by similarity descending and limit to TOP_K
            results.sort(key=lambda x: x.similarity_score, reverse=True)
            return results[: self.top_k]

        except (RAGProviderUnavailableError, RAGRetrievalError):
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"RAG retrieval failed: {str(e)}", exc_info=True)
            raise RAGRetrievalError(f"Unexpected retrieval error: {str(e)}")

    def build_context(self, chunks: List[RetrievedChunk]) -> str:
        """
        Build a context string from retrieved chunks.

        Args:
            chunks: List of RetrievedChunk objects

        Returns:
            Formatted context string for the LLM
        """
        if not chunks:
            return ""

        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Chunk {i} - {chunk.document_title}, Page {chunk.page_number}]")
            context_parts.append(chunk.text)
            context_parts.append("")

        return "\n".join(context_parts)

    def build_citations(self, chunks: List[RetrievedChunk]) -> List[dict]:
        """
        Build citation list from retrieved chunks.

        Args:
            chunks: List of RetrievedChunk objects

        Returns:
            List of citation dictionaries
        """
        citations = []
        for chunk in chunks:
            citation = {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "document_title": chunk.document_title,
                "page_number": chunk.page_number,
                "excerpt": chunk.text[:300],  # Limit excerpt length
                "similarity_score": chunk.similarity_score,
            }
            citations.append(citation)

        return citations

    @staticmethod
    def _cosine_similarity(a: list, b: list) -> float:
        """Calculate cosine similarity between two vectors."""
        a = np.array(a)
        b = np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
