"""
Centralized validation layer for AI-generated legal responses.

This module provides deterministic validation of AI responses based on:
- Evidence from retrieved document chunks
- Citation quality and coverage
- Similarity scores
- Contextual consistency

All validation is deterministic and does not require additional LLM calls.
"""

from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfidenceLevel(str, Enum):
    """Confidence levels based on documentary evidence."""
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"


@dataclass
class CitationSource:
    """Structured citation source with metadata."""
    document_id: str
    document_title: str
    chunk_id: str
    page_number: Optional[int] = None
    excerpt: str = ""
    similarity_score: Optional[float] = None

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "document_id": self.document_id,
            "document_title": self.document_title,
            "chunk_id": self.chunk_id,
            "page_number": self.page_number,
            "excerpt": self.excerpt,
            "similarity_score": self.similarity_score,
        }


@dataclass
class ValidationResult:
    """Result of response validation."""
    confidence_score: int  # 0-100
    confidence_level: str  # HIGH, MODERATE, LOW
    evidence_sufficient: bool
    hallucination_risk: str  # LOW, MEDIUM, HIGH
    validation_reasons: List[str] = field(default_factory=list)
    citations: List[CitationSource] = field(default_factory=list)
    disclaimer: str = ""

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "confidence_score": self.confidence_score,
            "confidence_level": self.confidence_level,
            "evidence_sufficient": self.evidence_sufficient,
            "hallucination_risk": self.hallucination_risk,
            "validation_reasons": self.validation_reasons,
            "citations": [c.to_dict() for c in self.citations],
            "disclaimer": self.disclaimer,
        }


@dataclass
class ValidatedAIResponse:
    """AI response with validation metadata."""
    content: str
    validation: ValidationResult
    blocked: bool = False
    block_reason: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            "content": self.content,
            "validation": self.validation.to_dict(),
            "blocked": self.blocked,
            "block_reason": self.block_reason,
        }


class AIValidator:
    """
    Centralized validator for AI-generated legal responses.

    Confidence Score Formula (0-100):
    - Up to 30 points: Existence and quantity of sources
    - Up to 30 points: Chunk similarity scores
    - Up to 20 points: Citation coverage
    - Up to 10 points: Consistency between response and context
    - Up to 10 points: Context quality and completeness

    Confidence Levels:
    - 80-100: HIGH (strong documentary evidence)
    - 60-79: MODERATE (adequate evidence with some gaps)
    - 0-59: LOW (insufficient evidence)
    """

    # Configuration thresholds
    MIN_SIMILARITY_SCORE = 0.3  # Minimum similarity to consider a chunk relevant
    MIN_CONFIDENCE_SCORE = 60  # Minimum score to allow response
    MIN_CITATIONS = 1  # Minimum number of citations required
    MAX_CITATION_EXCERPT_LENGTH = 300  # Maximum characters in citation excerpt

    # Disclaimer text
    LEGAL_DISCLAIMER = (
        "Esta análise foi gerada com auxílio de inteligência artificial, "
        "com base nos documentos fornecidos, e não substitui a revisão de um profissional jurídico."
    )

    def __init__(
        self,
        min_similarity_score: float = MIN_SIMILARITY_SCORE,
        min_confidence_score: int = MIN_CONFIDENCE_SCORE,
        min_citations: int = MIN_CITATIONS,
        max_excerpt_length: int = MAX_CITATION_EXCERPT_LENGTH,
    ):
        """Initialize validator with configurable thresholds."""
        self.min_similarity_score = min_similarity_score
        self.min_confidence_score = min_confidence_score
        self.min_citations = min_citations
        self.max_excerpt_length = max_excerpt_length

    def validate(
        self,
        response_content: str,
        retrieved_chunks: List[dict],
        citations: Optional[List[dict]] = None,
        document_title: str = "Documento",
    ) -> ValidatedAIResponse:
        """
        Validate an AI response against retrieved document evidence.

        Args:
            response_content: The AI-generated response text
            retrieved_chunks: List of chunks retrieved from RAG
            citations: List of citations from the response
            document_title: Title of the source document

        Returns:
            ValidatedAIResponse with validation metadata
        """
        validation_reasons = []
        citations_list = []
        confidence_score = 0
        hallucination_risk = "LOW"
        evidence_sufficient = True
        blocked = False
        block_reason = None

        # Check for empty response
        if not response_content or not response_content.strip():
            validation_reasons.append("Resposta vazia ou inválida")
            evidence_sufficient = False
            blocked = True
            block_reason = "Resposta vazia gerada pela IA"
            hallucination_risk = "HIGH"
            confidence_score = 0
            logger.warning("Validation failed: empty response")
            return self._create_response(
                response_content,
                confidence_score,
                evidence_sufficient,
                hallucination_risk,
                validation_reasons,
                citations_list,
                blocked,
                block_reason,
            )

        # Check for retrieved chunks
        if not retrieved_chunks or len(retrieved_chunks) == 0:
            validation_reasons.append("Nenhum chunk recuperado dos documentos")
            evidence_sufficient = False
            blocked = True
            block_reason = "Não encontrei evidências suficientes nos documentos selecionados para responder com segurança."
            hallucination_risk = "HIGH"
            confidence_score = 0
            logger.warning("Validation failed: no chunks retrieved")
            return self._create_response(
                response_content,
                confidence_score,
                evidence_sufficient,
                hallucination_risk,
                validation_reasons,
                citations_list,
                blocked,
                block_reason,
            )

        # Calculate confidence score based on evidence
        score_breakdown = self._calculate_confidence_score(
            retrieved_chunks, citations
        )
        confidence_score = score_breakdown["total"]
        validation_reasons.extend(score_breakdown["reasons"])

        # Process citations
        if citations:
            citations_list = self._process_citations(
                citations, retrieved_chunks, document_title
            )

        # Check citation requirements
        if len(citations_list) < self.min_citations:
            validation_reasons.append(
                f"Número insuficiente de citações ({len(citations_list)}/{self.min_citations})"
            )
            evidence_sufficient = False
            hallucination_risk = "MEDIUM"

        # Determine hallucination risk
        if confidence_score >= 80:
            hallucination_risk = "LOW"
        elif confidence_score >= 60:
            hallucination_risk = "MEDIUM"
        else:
            hallucination_risk = "HIGH"

        # Block if confidence is too low
        if confidence_score < self.min_confidence_score:
            evidence_sufficient = False
            blocked = True
            block_reason = "Não encontrei evidências suficientes nos documentos selecionados para responder com segurança."
            logger.warning(
                f"Validation blocked: confidence score {confidence_score} below threshold {self.min_confidence_score}"
            )

        return self._create_response(
            response_content,
            confidence_score,
            evidence_sufficient,
            hallucination_risk,
            validation_reasons,
            citations_list,
            blocked,
            block_reason,
        )

    def _calculate_confidence_score(
        self, retrieved_chunks: List[dict], citations: Optional[List[dict]] = None
    ) -> dict:
        """
        Calculate confidence score based on evidence.

        Returns dict with 'total' score (0-100) and 'reasons' list.
        """
        score = 0
        reasons = []

        # 1. Source existence and quantity (up to 30 points)
        chunk_count = len(retrieved_chunks) if retrieved_chunks else 0
        if chunk_count == 0:
            source_score = 0
            reasons.append("Nenhuma fonte recuperada")
        elif chunk_count == 1:
            source_score = 10
            reasons.append("Uma fonte recuperada")
        elif chunk_count <= 3:
            source_score = 20
            reasons.append(f"{chunk_count} fontes recuperadas")
        else:
            source_score = 30
            reasons.append(f"{chunk_count} fontes recuperadas (múltiplas)")

        score += source_score

        # 2. Similarity scores (up to 30 points)
        if retrieved_chunks:
            similarities = [
                float(chunk.get("similarity_score", 0))
                for chunk in retrieved_chunks
                if chunk.get("similarity_score")
            ]

            if similarities:
                avg_similarity = sum(similarities) / len(similarities)
                if avg_similarity >= 0.8:
                    similarity_score = 30
                    reasons.append(f"Similaridade alta (média: {avg_similarity:.2f})")
                elif avg_similarity >= 0.6:
                    similarity_score = 20
                    reasons.append(f"Similaridade moderada (média: {avg_similarity:.2f})")
                elif avg_similarity >= self.min_similarity_score:
                    similarity_score = 10
                    reasons.append(f"Similaridade baixa (média: {avg_similarity:.2f})")
                else:
                    similarity_score = 0
                    reasons.append(f"Similaridade insuficiente (média: {avg_similarity:.2f})")
            else:
                similarity_score = 0
                reasons.append("Scores de similaridade não disponíveis")

            score += similarity_score

        # 3. Citation coverage (up to 20 points)
        if citations and len(citations) > 0:
            if len(citations) >= 3:
                citation_score = 20
                reasons.append(f"Cobertura de citações completa ({len(citations)} citações)")
            elif len(citations) >= 1:
                citation_score = 10
                reasons.append(f"Cobertura de citações parcial ({len(citations)} citação(ões))")
            else:
                citation_score = 0
                reasons.append("Sem citações")
        else:
            citation_score = 0
            reasons.append("Sem citações fornecidas")

        score += citation_score

        # 4. Consistency (up to 10 points)
        # This is a heuristic: if we have good sources and citations, assume consistency
        if source_score >= 20 and citation_score >= 10:
            consistency_score = 10
            reasons.append("Consistência entre resposta e contexto")
        else:
            consistency_score = 0

        score += consistency_score

        # 5. Context quality (up to 10 points)
        # Check if chunks have meaningful content
        meaningful_chunks = sum(
            1
            for chunk in retrieved_chunks
            if chunk.get("text") and len(chunk.get("text", "")) > 50
        )

        if meaningful_chunks >= chunk_count * 0.8:
            context_score = 10
            reasons.append("Qualidade de contexto adequada")
        elif meaningful_chunks > 0:
            context_score = 5
            reasons.append("Qualidade de contexto parcial")
        else:
            context_score = 0
            reasons.append("Contexto insuficiente")

        score += context_score

        # Ensure score is within bounds
        score = max(0, min(100, score))

        return {"total": score, "reasons": reasons}

    def _process_citations(
        self,
        citations: List[dict],
        retrieved_chunks: List[dict],
        document_title: str,
    ) -> List[CitationSource]:
        """
        Process and structure citations from response.

        Removes duplicates, limits excerpt length, and orders by relevance.
        """
        processed = []
        seen = set()

        for citation in citations:
            if not isinstance(citation, dict):
                continue

            chunk_id = citation.get("chunk_id")
            if not chunk_id or chunk_id in seen:
                continue

            seen.add(chunk_id)

            # Find matching chunk for metadata
            matching_chunk = next(
                (c for c in retrieved_chunks if c.get("id") == chunk_id), None
            )

            excerpt = citation.get("text", "")
            if len(excerpt) > self.max_excerpt_length:
                excerpt = excerpt[: self.max_excerpt_length - 3] + "..."

            source = CitationSource(
                document_id=citation.get("document_id", ""),
                document_title=citation.get("document_title", document_title),
                chunk_id=chunk_id,
                page_number=matching_chunk.get("page_number") if matching_chunk else None,
                excerpt=excerpt,
                similarity_score=matching_chunk.get("similarity_score")
                if matching_chunk
                else None,
            )

            processed.append(source)

        # Sort by similarity score (descending)
        processed.sort(
            key=lambda x: x.similarity_score or 0, reverse=True
        )

        return processed

    def _create_response(
        self,
        content: str,
        confidence_score: int,
        evidence_sufficient: bool,
        hallucination_risk: str,
        validation_reasons: List[str],
        citations: List[CitationSource],
        blocked: bool,
        block_reason: Optional[str],
    ) -> ValidatedAIResponse:
        """Create a ValidatedAIResponse object."""
        # Determine confidence level
        if confidence_score >= 80:
            confidence_level = ConfidenceLevel.HIGH.value
        elif confidence_score >= 60:
            confidence_level = ConfidenceLevel.MODERATE.value
        else:
            confidence_level = ConfidenceLevel.LOW.value

        validation = ValidationResult(
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            evidence_sufficient=evidence_sufficient,
            hallucination_risk=hallucination_risk,
            validation_reasons=validation_reasons,
            citations=citations,
            disclaimer=self.LEGAL_DISCLAIMER,
        )

        # If blocked, clear content
        response_content = "" if blocked else content

        return ValidatedAIResponse(
            content=response_content,
            validation=validation,
            blocked=blocked,
            block_reason=block_reason,
        )

    @staticmethod
    def get_default_validator() -> "AIValidator":
        """Get a validator with default configuration."""
        return AIValidator()
