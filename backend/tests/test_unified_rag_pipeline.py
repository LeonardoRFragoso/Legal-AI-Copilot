"""
Tests for unified RAG pipeline.

Verifies that:
1. Only one retrieval is performed per question
2. The same chunks are used throughout the pipeline
3. Questions without evidence don't call the LLM
4. Citations are complete and traceable
5. Invalid citations are rejected
6. Provider errors are differentiated from no evidence
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from app.agent_executor import execute_question_answering
from app.rag_service import RAGService, RetrievedChunk, RAGProviderUnavailableError, RAGRetrievalError
from app.legal_agent import LegalAgent
from app.ai_validator import AIValidator, CitationSource, ValidatedAIResponse, ValidationResult
from sqlalchemy.orm import Session


class TestUnifiedRAGPipeline:
    """Test suite for unified RAG pipeline."""

    @pytest.fixture
    def mock_db(self):
        """Create a mock database session."""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_chunks(self):
        """Create sample retrieved chunks."""
        return [
            RetrievedChunk(
                chunk_id="chunk1",
                document_id="doc1",
                document_title="Contrato",
                page_number=1,
                text="O valor total do contrato é R$ 50.000",
                similarity_score=0.84,
            ),
            RetrievedChunk(
                chunk_id="chunk2",
                document_id="doc1",
                document_title="Contrato",
                page_number=2,
                text="Prazo de execução: 30 dias",
                similarity_score=0.76,
            ),
        ]

    def test_single_retrieval_per_question(self, mock_db, sample_chunks):
        """Test that retrieve() is called exactly once per question."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = sample_chunks
            mock_rag.build_context.return_value = "Contexto formatado"
            mock_rag.build_citations.return_value = [
                {
                    "chunk_id": "chunk1",
                    "document_id": "doc1",
                    "document_title": "Contrato",
                    "page_number": 1,
                    "excerpt": "O valor total do contrato é R$ 50.000",
                    "similarity_score": 0.84,
                }
            ]

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent
                mock_agent.answer_with_context.return_value = "O valor é R$ 50.000"

                with patch('app.agent_executor.AIValidator') as MockValidator:
                    mock_validator = Mock()
                    MockValidator.get_default_validator.return_value = mock_validator
                    mock_validator.validate.return_value = ValidatedAIResponse(
                        content="O valor é R$ 50.000",
                        validation=ValidationResult(
                            confidence_score=85,
                            confidence_level="high",
                            evidence_sufficient=True,
                            hallucination_risk="LOW",
                            validation_reasons=["Good evidence"],
                            citations=[],
                            disclaimer="Test",
                        ),
                        blocked=False,
                        block_reason=None,
                    )

                    result = execute_question_answering(
                        mock_db,
                        "Qual é o valor?",
                        [],
                        "doc1",
                        mock_agent,
                    )

            # Verify retrieve() was called exactly once
            mock_rag.retrieve.assert_called_once_with("Qual é o valor?", "doc1")

    def test_no_agent_executor_in_qa_flow(self, mock_db, sample_chunks):
        """Test that AgentExecutor is NOT used in QA flow."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = sample_chunks
            mock_rag.build_context.return_value = "Contexto"
            mock_rag.build_citations.return_value = []

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent
                # answer_with_context should be called, NOT query()
                mock_agent.answer_with_context.return_value = "Resposta"

                with patch('app.agent_executor.AIValidator') as MockValidator:
                    mock_validator = Mock()
                    MockValidator.get_default_validator.return_value = mock_validator
                    mock_validator.validate.return_value = ValidatedAIResponse(
                        content="Resposta",
                        validation=ValidationResult(
                            confidence_score=70,
                            confidence_level="moderate",
                            evidence_sufficient=True,
                            hallucination_risk="LOW",
                            validation_reasons=[],
                            citations=[],
                            disclaimer="Test",
                        ),
                        blocked=False,
                        block_reason=None,
                    )

                    result = execute_question_answering(
                        mock_db,
                        "Pergunta?",
                        [],
                        "doc1",
                        mock_agent,
                    )

            # Verify answer_with_context was called
            mock_agent.answer_with_context.assert_called_once()
            # Verify query() was NOT called
            mock_agent.query.assert_not_called()

    def test_same_chunks_throughout_pipeline(self, mock_db, sample_chunks):
        """Test that the same chunks are used by LLM and validator."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = sample_chunks
            mock_rag.build_context.return_value = "Contexto"
            mock_rag.build_citations.return_value = [
                {
                    "chunk_id": "chunk1",
                    "document_id": "doc1",
                    "document_title": "Contrato",
                    "page_number": 1,
                    "excerpt": "O valor total do contrato é R$ 50.000",
                    "similarity_score": 0.84,
                }
            ]

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent
                mock_agent.answer_with_context.return_value = "Resposta"

                with patch('app.agent_executor.AIValidator') as MockValidator:
                    mock_validator = Mock()
                    MockValidator.get_default_validator.return_value = mock_validator
                    mock_validator.validate.return_value = ValidatedAIResponse(
                        content="Resposta",
                        validation=ValidationResult(
                            confidence_score=85,
                            confidence_level="high",
                            evidence_sufficient=True,
                            hallucination_risk="LOW",
                            validation_reasons=[],
                            citations=[],
                            disclaimer="Test",
                        ),
                        blocked=False,
                        block_reason=None,
                    )

                    result = execute_question_answering(
                        mock_db,
                        "Pergunta?",
                        [],
                        "doc1",
                        mock_agent,
                    )

            # Verify validator received the same chunks
            call_args = mock_validator.validate.call_args
            validated_chunks = call_args[1]["retrieved_chunks"]
            assert len(validated_chunks) == 2
            assert validated_chunks[0]["chunk_id"] == "chunk1"
            assert validated_chunks[1]["chunk_id"] == "chunk2"

    def test_no_evidence_blocks_llm(self, mock_db):
        """Test that LLM is NOT called when no evidence is found."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = []  # No chunks

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent

                result = execute_question_answering(
                    mock_db,
                    "Pergunta sem evidência?",
                    [],
                    "doc1",
                    mock_agent,
                )

            # Verify LLM was NOT called
            mock_agent.answer_with_context.assert_not_called()
            # Verify response is blocked
            assert result["blocked"] is True
            assert result["error"] == "NO_EVIDENCE"

    def test_citation_completeness(self, mock_db, sample_chunks):
        """Test that citations have all required fields."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = sample_chunks
            mock_rag.build_context.return_value = "Contexto"
            mock_rag.build_citations.return_value = [
                {
                    "chunk_id": "chunk1",
                    "document_id": "doc1",
                    "document_title": "Contrato",
                    "page_number": 1,
                    "excerpt": "O valor total do contrato é R$ 50.000",
                    "similarity_score": 0.84,
                }
            ]

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent
                mock_agent.answer_with_context.return_value = "Resposta"

                with patch('app.agent_executor.AIValidator') as MockValidator:
                    mock_validator = Mock()
                    MockValidator.get_default_validator.return_value = mock_validator
                    
                    # Create a citation source with all required fields
                    citation = CitationSource(
                        document_id="doc1",
                        document_title="Contrato",
                        chunk_id="chunk1",
                        page_number=1,
                        excerpt="O valor total do contrato é R$ 50.000",
                        similarity_score=0.84,
                    )
                    
                    mock_validator.validate.return_value = ValidatedAIResponse(
                        content="Resposta",
                        validation=ValidationResult(
                            confidence_score=85,
                            confidence_level="high",
                            evidence_sufficient=True,
                            hallucination_risk="LOW",
                            validation_reasons=[],
                            citations=[citation],
                            disclaimer="Test",
                        ),
                        blocked=False,
                        block_reason=None,
                    )

                    result = execute_question_answering(
                        mock_db,
                        "Pergunta?",
                        [],
                        "doc1",
                        mock_agent,
                    )

            # Verify citation has all required fields
            assert len(result["citations"]) == 1
            citation_dict = result["citations"][0]
            assert "chunk_id" in citation_dict
            assert "document_id" in citation_dict
            assert "document_title" in citation_dict
            assert "page_number" in citation_dict
            assert "excerpt" in citation_dict
            assert citation_dict["excerpt"] != ""
            assert "similarity_score" in citation_dict

    def test_invalid_citation_rejected(self, mock_db, sample_chunks):
        """Test that citations without matching chunks are rejected."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = sample_chunks
            mock_rag.build_context.return_value = "Contexto"
            # Citation with non-existent chunk_id
            mock_rag.build_citations.return_value = [
                {
                    "chunk_id": "nonexistent",
                    "document_id": "doc1",
                    "document_title": "Contrato",
                    "page_number": 1,
                    "excerpt": "Trecho",
                    "similarity_score": 0.5,
                }
            ]

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent
                mock_agent.answer_with_context.return_value = "Resposta"

                with patch('app.agent_executor.AIValidator') as MockValidator:
                    mock_validator = Mock()
                    MockValidator.get_default_validator.return_value = mock_validator
                    # Validator should reject invalid citation
                    mock_validator.validate.return_value = ValidatedAIResponse(
                        content="",
                        validation=ValidationResult(
                            confidence_score=0,
                            confidence_level="low",
                            evidence_sufficient=False,
                            hallucination_risk="HIGH",
                            validation_reasons=["Citação inválida"],
                            citations=[],
                            disclaimer="Test",
                        ),
                        blocked=True,
                        block_reason="Citação sem correspondência",
                    )

                    result = execute_question_answering(
                        mock_db,
                        "Pergunta?",
                        [],
                        "doc1",
                        mock_agent,
                    )

            # Verify response is blocked
            assert result["blocked"] is True

    def test_provider_unavailable_error(self, mock_db):
        """Test that provider unavailability is handled separately from no evidence."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            # Simulate provider error
            mock_rag.retrieve.side_effect = RAGProviderUnavailableError("API key invalid")

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent

                result = execute_question_answering(
                    mock_db,
                    "Pergunta?",
                    [],
                    "doc1",
                    mock_agent,
                )

            # Verify error is AI_PROVIDER_UNAVAILABLE, not NO_EVIDENCE
            assert result["error"] == "AI_PROVIDER_UNAVAILABLE"
            assert "temporariamente indisponível" in result["content"]
            # Verify LLM was NOT called
            mock_agent.answer_with_context.assert_not_called()

    def test_retrieval_error(self, mock_db):
        """Test that retrieval errors are handled separately."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            # Simulate retrieval error
            mock_rag.retrieve.side_effect = RAGRetrievalError("Database error")

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent

                result = execute_question_answering(
                    mock_db,
                    "Pergunta?",
                    [],
                    "doc1",
                    mock_agent,
                )

            # Verify error is RAG_RETRIEVAL_FAILED
            assert result["error"] == "RAG_RETRIEVAL_FAILED"
            # Verify LLM was NOT called
            mock_agent.answer_with_context.assert_not_called()

    def test_answer_with_context_called_with_correct_params(self, mock_db, sample_chunks):
        """Test that answer_with_context is called with query and context."""
        with patch('app.agent_executor.RAGService') as MockRAGService:
            mock_rag = Mock()
            MockRAGService.return_value = mock_rag
            mock_rag.retrieve.return_value = sample_chunks
            expected_context = "Contexto formatado"
            mock_rag.build_context.return_value = expected_context
            mock_rag.build_citations.return_value = []

            with patch('app.agent_executor.LegalAgent') as MockAgent:
                mock_agent = Mock()
                MockAgent.return_value = mock_agent
                mock_agent.answer_with_context.return_value = "Resposta"

                with patch('app.agent_executor.AIValidator') as MockValidator:
                    mock_validator = Mock()
                    MockValidator.get_default_validator.return_value = mock_validator
                    mock_validator.validate.return_value = ValidatedAIResponse(
                        content="Resposta",
                        validation=ValidationResult(
                            confidence_score=70,
                            confidence_level="moderate",
                            evidence_sufficient=True,
                            hallucination_risk="LOW",
                            validation_reasons=[],
                            citations=[],
                            disclaimer="Test",
                        ),
                        blocked=False,
                        block_reason=None,
                    )

                    query = "Qual é o valor?"
                    result = execute_question_answering(
                        mock_db,
                        query,
                        [],
                        "doc1",
                        mock_agent,
                    )

            # Verify answer_with_context was called with correct parameters
            call_args = mock_agent.answer_with_context.call_args
            assert call_args[0][0] == query  # First positional arg is query
            assert call_args[0][1] == expected_context  # Second positional arg is context
