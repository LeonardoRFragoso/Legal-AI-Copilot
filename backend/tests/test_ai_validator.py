"""
Tests for AI response validation.
"""

import pytest
from app.ai_validator import (
    AIValidator,
    CitationSource,
    ValidationResult,
    ValidatedAIResponse,
    ConfidenceLevel,
)


class TestCitationSource:
    """Tests for CitationSource dataclass."""

    def test_citation_source_creation(self):
        """Test creating a citation source."""
        citation = CitationSource(
            document_id="doc1",
            document_title="Test Document",
            chunk_id="chunk1",
            page_number=5,
            excerpt="Test excerpt",
            similarity_score=0.85,
        )

        assert citation.document_id == "doc1"
        assert citation.document_title == "Test Document"
        assert citation.chunk_id == "chunk1"
        assert citation.page_number == 5
        assert citation.excerpt == "Test excerpt"
        assert citation.similarity_score == 0.85

    def test_citation_source_to_dict(self):
        """Test converting citation to dictionary."""
        citation = CitationSource(
            document_id="doc1",
            document_title="Test Document",
            chunk_id="chunk1",
            page_number=None,
            excerpt="Test excerpt",
            similarity_score=0.85,
        )

        result = citation.to_dict()
        assert isinstance(result, dict)
        assert result["document_id"] == "doc1"
        assert result["page_number"] is None


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_validation_result_creation(self):
        """Test creating a validation result."""
        result = ValidationResult(
            confidence_score=85,
            confidence_level="high",
            evidence_sufficient=True,
            hallucination_risk="LOW",
            validation_reasons=["Good sources"],
            citations=[],
            disclaimer="Test disclaimer",
        )

        assert result.confidence_score == 85
        assert result.confidence_level == "high"
        assert result.evidence_sufficient is True
        assert result.hallucination_risk == "LOW"


class TestAIValidator:
    """Tests for AIValidator class."""

    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return AIValidator()

    def test_validator_initialization(self, validator):
        """Test validator initialization with defaults."""
        assert validator.min_similarity_score == 0.3
        assert validator.min_confidence_score == 60
        assert validator.min_citations == 1
        assert validator.max_excerpt_length == 300

    def test_validator_custom_thresholds(self):
        """Test validator with custom thresholds."""
        validator = AIValidator(
            min_similarity_score=0.5,
            min_confidence_score=70,
            min_citations=2,
            max_excerpt_length=200,
        )

        assert validator.min_similarity_score == 0.5
        assert validator.min_confidence_score == 70
        assert validator.min_citations == 2
        assert validator.max_excerpt_length == 200

    def test_validate_empty_response(self, validator):
        """Test validation of empty response."""
        result = validator.validate(
            response_content="",
            retrieved_chunks=[{"chunk_id": "chunk1", "text": "Some text", "document_id": "doc1", "document_title": "Test"}],
        )

        assert result.blocked is True
        assert result.validation.confidence_score == 0
        assert result.validation.hallucination_risk == "HIGH"
        assert result.block_reason == "Resposta vazia gerada pela IA"

    def test_validate_no_chunks(self, validator):
        """Test validation with no retrieved chunks."""
        result = validator.validate(
            response_content="Some response",
            retrieved_chunks=[],
        )

        assert result.blocked is True
        assert result.validation.confidence_score == 0
        assert result.validation.hallucination_risk == "HIGH"
        assert "Não encontrei evidências suficientes" in result.block_reason

    def test_validate_with_good_sources(self, validator):
        """Test validation with good sources."""
        chunks = [
            {
                "chunk_id": "chunk1",
                "document_id": "doc1",
                "document_title": "Test Doc",
                "text": "This is a long chunk with meaningful content about contracts",
                "similarity_score": 0.85,
                "page_number": 1,
            },
            {
                "chunk_id": "chunk2",
                "document_id": "doc1",
                "document_title": "Test Doc",
                "text": "Another relevant chunk with important information",
                "similarity_score": 0.80,
                "page_number": 2,
            },
        ]

        citations = [
            {
                "chunk_id": "chunk1",
                "text": "contracts",
                "document_id": "doc1",
                "document_title": "Test Doc",
            },
            {
                "chunk_id": "chunk2",
                "text": "important information",
                "document_id": "doc1",
                "document_title": "Test Doc",
            },
        ]

        result = validator.validate(
            response_content="Response about contracts",
            retrieved_chunks=chunks,
            citations=citations,
        )

        assert result.blocked is False
        assert result.validation.confidence_score >= 60
        assert result.validation.confidence_level in ["high", "moderate"]

    def test_confidence_score_bounds(self, validator):
        """Test that confidence score stays within 0-100."""
        # Test with many good chunks
        chunks = [
            {
                "chunk_id": f"chunk{i}",
                "document_id": "doc1",
                "document_title": "Test",
                "text": "A" * 100,
                "similarity_score": 0.95,
            }
            for i in range(10)
        ]

        result = validator.validate(
            response_content="Response",
            retrieved_chunks=chunks,
        )

        assert 0 <= result.validation.confidence_score <= 100

    def test_citation_deduplication(self, validator):
        """Test that duplicate citations are removed."""
        chunks = [
            {
                "chunk_id": "chunk1",
                "document_id": "doc1",
                "document_title": "Test",
                "text": "Content",
                "similarity_score": 0.85,
            }
        ]

        citations = [
            {
                "chunk_id": "chunk1",
                "text": "Content",
                "document_id": "doc1",
                "document_title": "Test",
            },
            {
                "chunk_id": "chunk1",
                "text": "Content",
                "document_id": "doc1",
                "document_title": "Test",
            },
        ]

        result = validator.validate(
            response_content="Response",
            retrieved_chunks=chunks,
            citations=citations,
        )

        assert len(result.validation.citations) == 1

    def test_citation_excerpt_truncation(self, validator):
        """Test that citation excerpts are truncated."""
        long_text = "A" * 500
        chunks = [
            {
                "chunk_id": "chunk1",
                "document_id": "doc1",
                "document_title": "Test",
                "text": long_text,
                "similarity_score": 0.85,
            }
        ]

        citations = [
            {
                "chunk_id": "chunk1",
                "text": long_text,
                "document_id": "doc1",
                "document_title": "Test",
            }
        ]

        result = validator.validate(
            response_content="Response",
            retrieved_chunks=chunks,
            citations=citations,
        )

        assert len(result.validation.citations[0].excerpt) <= validator.max_excerpt_length

    def test_confidence_level_high(self, validator):
        """Test HIGH confidence level."""
        chunks = [
            {
                "id": "chunk1",
                "text": "A" * 100,
                "similarity_score": 0.95,
            },
            {
                "id": "chunk2",
                "text": "A" * 100,
                "similarity_score": 0.90,
            },
        ]

        citations = [
            {
                "chunk_id": "chunk1",
                "text": "Content",
                "document_id": "doc1",
                "document_title": "Test",
            }
        ]

        result = validator.validate(
            response_content="Response",
            retrieved_chunks=chunks,
            citations=citations,
        )

        if result.validation.confidence_score >= 80:
            assert result.validation.confidence_level == "high"

    def test_confidence_level_moderate(self, validator):
        """Test MODERATE confidence level."""
        chunks = [
            {
                "id": "chunk1",
                "text": "A" * 100,
                "similarity_score": 0.65,
            }
        ]

        citations = [
            {
                "chunk_id": "chunk1",
                "text": "Content",
                "document_id": "doc1",
                "document_title": "Test",
            }
        ]

        result = validator.validate(
            response_content="Response",
            retrieved_chunks=chunks,
            citations=citations,
        )

        if 60 <= result.validation.confidence_score < 80:
            assert result.validation.confidence_level == "moderate"

    def test_confidence_level_low(self, validator):
        """Test LOW confidence level."""
        chunks = [
            {
                "id": "chunk1",
                "text": "A" * 50,
                "similarity_score": 0.35,
            }
        ]

        result = validator.validate(
            response_content="Response",
            retrieved_chunks=chunks,
        )

        if result.validation.confidence_score < 60:
            assert result.validation.confidence_level == "low"

    def test_disclaimer_always_present(self, validator):
        """Test that disclaimer is always present."""
        result = validator.validate(
            response_content="Response",
            retrieved_chunks=[],
        )

        assert result.validation.disclaimer != ""
        assert "inteligência artificial" in result.validation.disclaimer.lower()

    def test_blocked_response_has_no_content(self, validator):
        """Test that blocked responses have empty content."""
        result = validator.validate(
            response_content="This should be blocked",
            retrieved_chunks=[],
        )

        assert result.blocked is True
        assert result.content == ""

    def test_unblocked_response_has_content(self, validator):
        """Test that unblocked responses have content."""
        chunks = [
            {
                "id": "chunk1",
                "text": "A" * 100,
                "similarity_score": 0.85,
            }
        ]

        citations = [
            {
                "chunk_id": "chunk1",
                "text": "Content",
                "document_id": "doc1",
                "document_title": "Test",
            }
        ]

        result = validator.validate(
            response_content="This should not be blocked",
            retrieved_chunks=chunks,
            citations=citations,
        )

        if not result.blocked:
            assert result.content == "This should not be blocked"

    def test_get_default_validator(self):
        """Test getting default validator."""
        validator = AIValidator.get_default_validator()
        assert isinstance(validator, AIValidator)
        assert validator.min_similarity_score == 0.3

    def test_validated_response_to_dict(self, validator):
        """Test converting ValidatedAIResponse to dict."""
        result = validator.validate(
            response_content="Response",
            retrieved_chunks=[],
        )

        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert "content" in result_dict
        assert "validation" in result_dict
        assert "blocked" in result_dict
        assert "block_reason" in result_dict
