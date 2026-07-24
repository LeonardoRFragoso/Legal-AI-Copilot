"""
Tests for Agent Router.
"""

import pytest
from app.agent_router import (
    LegalAgentRouter,
    AgentIntent,
    RouterDecision,
)


class TestAgentIntent:
    """Tests for AgentIntent enum."""

    def test_intent_values(self):
        """Test that all intents have correct values."""
        assert AgentIntent.SUMMARIZE_DOCUMENT.value == "summarize_document"
        assert AgentIntent.EXTRACT_INFORMATION.value == "extract_information"
        assert AgentIntent.COMPARE_DOCUMENTS.value == "compare_documents"
        assert AgentIntent.QUESTION_ANSWERING.value == "question_answering"
        assert AgentIntent.IDENTIFY_RISKS.value == "identify_risks"
        assert AgentIntent.UNKNOWN.value == "unknown"


class TestRouterDecision:
    """Tests for RouterDecision dataclass."""

    def test_decision_creation(self):
        """Test creating a router decision."""
        decision = RouterDecision(
            intent=AgentIntent.SUMMARIZE_DOCUMENT,
            tool="summarize_document",
            reason="User requested summary",
            required_documents=["doc1"],
            confidence=0.95,
        )

        assert decision.intent == AgentIntent.SUMMARIZE_DOCUMENT
        assert decision.tool == "summarize_document"
        assert decision.confidence == 0.95


class TestLegalAgentRouter:
    """Tests for LegalAgentRouter."""

    @pytest.fixture
    def router(self):
        """Create a router instance."""
        return LegalAgentRouter()

    def test_router_initialization(self, router):
        """Test router initialization."""
        assert isinstance(router, LegalAgentRouter)

    def test_summarize_intent(self, router):
        """Test summarization intent detection."""
        decision = router.route("faça um resumo do contrato")
        assert decision.intent == AgentIntent.SUMMARIZE_DOCUMENT
        assert decision.tool == "summarize_document"
        assert decision.confidence >= 0.9

    def test_summarize_intent_english(self, router):
        """Test summarization intent in English."""
        decision = router.route("provide a summary of the document")
        assert decision.intent == AgentIntent.SUMMARIZE_DOCUMENT

    def test_extract_intent(self, router):
        """Test extraction intent detection."""
        decision = router.route("extraia as partes do contrato")
        assert decision.intent == AgentIntent.EXTRACT_INFORMATION
        assert decision.tool == "extract_information"

    def test_extract_intent_english(self, router):
        """Test extraction intent in English."""
        decision = router.route("extract the parties and dates")
        assert decision.intent == AgentIntent.EXTRACT_INFORMATION

    def test_compare_intent(self, router):
        """Test comparison intent detection."""
        decision = router.route("compare estes dois contratos")
        assert decision.intent == AgentIntent.COMPARE_DOCUMENTS
        assert decision.tool == "compare_documents"

    def test_compare_intent_english(self, router):
        """Test comparison intent in English."""
        decision = router.route("compare the two documents")
        assert decision.intent == AgentIntent.COMPARE_DOCUMENTS

    def test_risk_intent(self, router):
        """Test risk analysis intent detection."""
        decision = router.route("quais são os riscos deste contrato")
        assert decision.intent == AgentIntent.IDENTIFY_RISKS
        assert decision.tool == "contract_risk_analysis"

    def test_risk_intent_english(self, router):
        """Test risk analysis intent in English."""
        decision = router.route("identify risks in this contract")
        assert decision.intent == AgentIntent.IDENTIFY_RISKS

    def test_question_intent(self, router):
        """Test question answering intent detection."""
        decision = router.route("qual é o valor do contrato?")
        assert decision.intent == AgentIntent.QUESTION_ANSWERING
        assert decision.tool == "semantic_search"

    def test_question_intent_english(self, router):
        """Test question intent in English."""
        decision = router.route("what is the contract value?")
        assert decision.intent == AgentIntent.QUESTION_ANSWERING

    def test_unknown_intent(self, router):
        """Test unknown intent detection."""
        decision = router.route("xyz abc def")
        assert decision.intent == AgentIntent.UNKNOWN

    def test_required_documents_single(self, router):
        """Test required documents for single-document tools."""
        decision = router.route(
            "faça um resumo",
            available_documents=["doc1", "doc2"]
        )
        assert len(decision.required_documents) <= 1

    def test_required_documents_multiple(self, router):
        """Test required documents for multi-document tools."""
        decision = router.route(
            "compare os documentos",
            available_documents=["doc1", "doc2", "doc3"]
        )
        assert decision.intent == AgentIntent.COMPARE_DOCUMENTS
        assert len(decision.required_documents) <= 2

    def test_no_available_documents(self, router):
        """Test routing with no available documents."""
        decision = router.route("faça um resumo")
        assert decision.intent == AgentIntent.SUMMARIZE_DOCUMENT
        assert len(decision.required_documents) == 0

    def test_confidence_scores(self, router):
        """Test that confidence scores are reasonable."""
        decision = router.route("faça um resumo")
        assert 0 <= decision.confidence <= 1

    def test_reason_provided(self, router):
        """Test that reason is always provided."""
        decision = router.route("faça um resumo")
        assert decision.reason != ""
        assert len(decision.reason) > 0

    def test_case_insensitive(self, router):
        """Test that routing is case insensitive."""
        decision1 = router.route("FAÇA UM RESUMO")
        decision2 = router.route("faça um resumo")
        assert decision1.intent == decision2.intent

    def test_whitespace_handling(self, router):
        """Test that whitespace is handled correctly."""
        decision1 = router.route("  faça um resumo  ")
        decision2 = router.route("faça um resumo")
        assert decision1.intent == decision2.intent

    def test_multiple_keywords(self, router):
        """Test handling of multiple keywords."""
        # Should match first detected intent
        decision = router.route("resumo e comparação")
        assert decision.intent in [
            AgentIntent.SUMMARIZE_DOCUMENT,
            AgentIntent.COMPARE_DOCUMENTS
        ]

    def test_risk_keywords_variations(self, router):
        """Test various risk-related keywords."""
        risk_queries = [
            "quais riscos",
            "identify risks",
            "problemas no contrato",
            "issues in contract",
            "cuidado com",
            "critical issues"
        ]

        for query in risk_queries:
            decision = router.route(query)
            assert decision.intent == AgentIntent.IDENTIFY_RISKS, f"Failed for: {query}"
