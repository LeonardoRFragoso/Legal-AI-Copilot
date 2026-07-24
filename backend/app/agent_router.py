"""
Agent Router for Legal AI Copilot.

Determines which tool/action to execute based on user intent.
Uses deterministic heuristics with optional LLM fallback.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
import re
import logging

logger = logging.getLogger(__name__)


class AgentIntent(str, Enum):
    """Enumeration of possible agent intents."""
    SUMMARIZE_DOCUMENT = "summarize_document"
    EXTRACT_INFORMATION = "extract_information"
    COMPARE_DOCUMENTS = "compare_documents"
    QUESTION_ANSWERING = "question_answering"
    IDENTIFY_RISKS = "identify_risks"
    UNKNOWN = "unknown"


@dataclass
class RouterDecision:
    """Decision made by the agent router."""
    intent: AgentIntent
    tool: str
    reason: str
    required_documents: List[str]
    confidence: float  # 0-1, confidence in the decision


class LegalAgentRouter:
    """
    Routes user requests to appropriate tools.

    Uses deterministic heuristics first, with optional LLM fallback.
    """

    # Keywords for intent classification
    SUMMARIZE_KEYWORDS = {
        "resumo", "summary", "resumir", "sintetizar", "síntese",
        "overview", "visão geral", "resumido", "condensado"
    }

    EXTRACT_KEYWORDS = {
        "extrair", "extract", "partes", "datas", "valores",
        "cláusulas", "informações", "dados", "detalhes",
        "parties", "dates", "amounts", "clauses"
    }

    COMPARE_KEYWORDS = {
        "comparar", "compare", "diferença", "diferenças",
        "similarity", "similarities", "semelhança", "semelhante",
        "versus", "vs", "contraste"
    }

    RISK_KEYWORDS = {
        "risco", "riscos", "risk", "risks", "perigo", "perigoso",
        "problema", "problemas", "issue", "issues", "cuidado",
        "atenção", "alerta", "crítico", "critical"
    }

    def __init__(self):
        """Initialize the router."""
        pass

    def route(
        self,
        user_input: str,
        available_documents: List[str] = None,
        conversation_context: Optional[str] = None,
    ) -> RouterDecision:
        """
        Route user input to appropriate tool.

        Args:
            user_input: User's request text
            available_documents: List of document IDs available
            conversation_context: Previous conversation context

        Returns:
            RouterDecision with intent, tool, and metadata
        """
        if available_documents is None:
            available_documents = []

        # Normalize input
        normalized_input = user_input.lower().strip()

        # Try deterministic classification first
        decision = self._classify_deterministic(
            normalized_input, available_documents
        )

        if decision.intent != AgentIntent.UNKNOWN:
            logger.info(
                f"Routed to {decision.intent.value} with confidence {decision.confidence}"
            )
            return decision

        # If deterministic fails, return UNKNOWN
        logger.warning(f"Could not classify intent for: {user_input}")
        return RouterDecision(
            intent=AgentIntent.UNKNOWN,
            tool="unknown",
            reason="Could not determine user intent",
            required_documents=[],
            confidence=0.0,
        )

    def _classify_deterministic(
        self, normalized_input: str, available_documents: List[str]
    ) -> RouterDecision:
        """
        Classify intent using deterministic heuristics.

        Returns RouterDecision with UNKNOWN intent if no match found.
        """
        # Check for summarization intent
        if self._matches_keywords(normalized_input, self.SUMMARIZE_KEYWORDS):
            return RouterDecision(
                intent=AgentIntent.SUMMARIZE_DOCUMENT,
                tool="summarize_document",
                reason="User requested document summary",
                required_documents=available_documents[:1] if available_documents else [],
                confidence=0.95,
            )

        # Check for extraction intent
        if self._matches_keywords(normalized_input, self.EXTRACT_KEYWORDS):
            return RouterDecision(
                intent=AgentIntent.EXTRACT_INFORMATION,
                tool="extract_information",
                reason="User requested information extraction",
                required_documents=available_documents[:1] if available_documents else [],
                confidence=0.95,
            )

        # Check for comparison intent
        if self._matches_keywords(normalized_input, self.COMPARE_KEYWORDS):
            return RouterDecision(
                intent=AgentIntent.COMPARE_DOCUMENTS,
                tool="compare_documents",
                reason="User requested document comparison",
                required_documents=available_documents[:2] if len(available_documents) >= 2 else available_documents,
                confidence=0.95,
            )

        # Check for risk analysis intent
        if self._matches_keywords(normalized_input, self.RISK_KEYWORDS):
            return RouterDecision(
                intent=AgentIntent.IDENTIFY_RISKS,
                tool="contract_risk_analysis",
                reason="User requested risk identification",
                required_documents=available_documents[:1] if available_documents else [],
                confidence=0.95,
            )

        # Default to question answering for other queries
        if self._is_question(normalized_input):
            return RouterDecision(
                intent=AgentIntent.QUESTION_ANSWERING,
                tool="semantic_search",
                reason="User asked a question",
                required_documents=available_documents[:1] if available_documents else [],
                confidence=0.85,
            )

        # Unknown intent
        return RouterDecision(
            intent=AgentIntent.UNKNOWN,
            tool="unknown",
            reason="Could not determine user intent",
            required_documents=[],
            confidence=0.0,
        )

    @staticmethod
    def _matches_keywords(text: str, keywords: set) -> bool:
        """
        Check if text contains any of the keywords.

        Uses word boundaries to avoid partial matches.
        """
        # Split text into words
        words = re.findall(r'\b\w+\b', text)
        
        # Check if any word matches keywords
        for word in words:
            if word in keywords:
                return True
        
        return False

    @staticmethod
    def _is_question(text: str) -> bool:
        """Check if text is a question."""
        # Simple heuristic: ends with ? or contains question words
        question_words = {
            "qual", "quais", "quando", "onde", "por que", "como",
            "what", "when", "where", "why", "how", "who", "whom"
        }

        # Check for question mark
        if text.strip().endswith("?"):
            return True

        # Check for question words
        words = re.findall(r'\b\w+\b', text)
        for word in words:
            if word in question_words:
                return True

        return False

    def to_dict(self) -> dict:
        """Convert decision to dictionary."""
        return {
            "intent": self.intent.value,
            "tool": self.tool,
            "reason": self.reason,
            "required_documents": self.required_documents,
            "confidence": self.confidence,
        }


def get_default_router() -> LegalAgentRouter:
    """Get a default router instance."""
    return LegalAgentRouter()
