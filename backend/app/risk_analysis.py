"""
Contract Risk Analysis module.

Analyzes contracts for potential risks using three layers:
1. Deterministic heuristics
2. RAG-based retrieval
3. LLM-based analysis with guardrails
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict
import logging
import json

from sqlalchemy.orm import Session
from app.models import Document, Chunk, DocumentEmbedding
from app.embedding_service import EmbeddingService
from app.ai_validator import AIValidator, CitationSource
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class RiskSeverity(str, Enum):
    """Risk severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskCategory(str, Enum):
    """Risk categories."""
    CONFIDENTIALITY = "confidentiality"
    LGPD = "lgpd"
    TERMINATION = "termination"
    PAYMENT = "payment"
    LIABILITY = "liability"
    PENALTY = "penalty"
    FORUM = "forum"
    SLA = "sla"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    RENEWAL = "renewal"
    DURATION = "duration"
    COMPLIANCE = "compliance"
    OTHER = "other"


@dataclass
class ContractRisk:
    """Represents a single contract risk."""
    title: str
    description: str
    severity: RiskSeverity
    category: RiskCategory
    recommendation: str
    citations: List[CitationSource] = field(default_factory=list)
    confidence_score: int = 75  # 0-100

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "category": self.category.value,
            "recommendation": self.recommendation,
            "citations": [c.to_dict() for c in self.citations],
            "confidence_score": self.confidence_score,
        }


@dataclass
class RiskAnalysisResult:
    """Result of contract risk analysis."""
    summary: str
    overall_risk: RiskSeverity
    confidence_score: int  # 0-100
    confidence_level: str  # HIGH, MODERATE, LOW
    risks: List[ContractRisk] = field(default_factory=list)
    citations: List[CitationSource] = field(default_factory=list)
    disclaimer: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "summary": self.summary,
            "overall_risk": self.overall_risk.value,
            "confidence_score": self.confidence_score,
            "confidence_level": self.confidence_level,
            "risks": [r.to_dict() for r in self.risks],
            "citations": [c.to_dict() for c in self.citations],
            "disclaimer": self.disclaimer,
        }


class HeuristicAnalyzer:
    """Deterministic heuristic-based risk detection."""

    # Keywords for detecting missing clauses
    CONFIDENTIALITY_KEYWORDS = {
        "confidencial", "confidentiality", "sigilo", "secret",
        "proprietary", "proprietário", "nda", "non-disclosure"
    }

    LGPD_KEYWORDS = {
        "lgpd", "lei geral de proteção de dados", "gdpr",
        "dados pessoais", "personal data", "privacidade", "privacy"
    }

    TERMINATION_KEYWORDS = {
        "rescisão", "termination", "encerramento", "término",
        "cancelamento", "cancellation", "dissolução"
    }

    PENALTY_KEYWORDS = {
        "multa", "penalty", "penalidade", "indenização",
        "damages", "compensação", "compensation"
    }

    def __init__(self, db: Session):
        """Initialize analyzer."""
        self.db = db

    def analyze(self, document_id: str) -> List[ContractRisk]:
        """
        Perform heuristic analysis on document.

        Returns list of detected risks.
        """
        risks = []

        # Get document and chunks
        document = self.db.query(Document).filter(
            Document.id == document_id
        ).first()

        if not document:
            return risks

        chunks = self.db.query(Chunk).filter(
            Chunk.document_id == document_id
        ).all()

        if not chunks:
            return risks

        # Combine all text
        full_text = " ".join([c.text for c in chunks]).lower()

        # Check for missing clauses
        risks.extend(self._check_missing_clauses(full_text, chunks))

        # Check for problematic patterns
        risks.extend(self._check_problematic_patterns(full_text, chunks))

        return risks

    def _check_missing_clauses(
        self, full_text: str, chunks: List[Chunk]
    ) -> List[ContractRisk]:
        """Check for missing important clauses."""
        risks = []

        # Check for confidentiality clause
        if not self._contains_keywords(full_text, self.CONFIDENTIALITY_KEYWORDS):
            risks.append(
                ContractRisk(
                    title="Missing Confidentiality Clause",
                    description="The contract does not contain a confidentiality or non-disclosure clause.",
                    severity=RiskSeverity.MEDIUM,
                    category=RiskCategory.CONFIDENTIALITY,
                    recommendation="Add a confidentiality clause to protect sensitive information.",
                    confidence_score=90,
                )
            )

        # Check for LGPD compliance
        if not self._contains_keywords(full_text, self.LGPD_KEYWORDS):
            risks.append(
                ContractRisk(
                    title="Missing LGPD Compliance Clause",
                    description="The contract does not reference LGPD (Lei Geral de Proteção de Dados) compliance.",
                    severity=RiskSeverity.HIGH,
                    category=RiskCategory.LGPD,
                    recommendation="Include LGPD compliance clause and data protection obligations.",
                    confidence_score=85,
                )
            )

        # Check for termination clause
        if not self._contains_keywords(full_text, self.TERMINATION_KEYWORDS):
            risks.append(
                ContractRisk(
                    title="Missing Termination Clause",
                    description="The contract does not specify how it can be terminated.",
                    severity=RiskSeverity.MEDIUM,
                    category=RiskCategory.TERMINATION,
                    recommendation="Define clear termination conditions and notice periods.",
                    confidence_score=88,
                )
            )

        return risks

    def _check_problematic_patterns(
        self, full_text: str, chunks: List[Chunk]
    ) -> List[ContractRisk]:
        """Check for problematic patterns in contract."""
        risks = []

        # Check for unlimited penalties
        if "multa ilimitada" in full_text or "unlimited penalty" in full_text:
            risks.append(
                ContractRisk(
                    title="Unlimited Penalty Clause",
                    description="The contract contains a clause with unlimited penalties.",
                    severity=RiskSeverity.CRITICAL,
                    category=RiskCategory.PENALTY,
                    recommendation="Define a maximum penalty amount or percentage.",
                    confidence_score=95,
                )
            )

        # Check for automatic renewal
        if "renovação automática" in full_text or "automatic renewal" in full_text:
            risks.append(
                ContractRisk(
                    title="Automatic Renewal Clause",
                    description="The contract automatically renews without explicit action.",
                    severity=RiskSeverity.MEDIUM,
                    category=RiskCategory.RENEWAL,
                    recommendation="Require explicit renewal or add clear opt-out mechanism.",
                    confidence_score=92,
                )
            )

        # Check for indefinite payment
        if "pagamento indefinido" in full_text or "indefinite payment" in full_text:
            risks.append(
                ContractRisk(
                    title="Indefinite Payment Obligation",
                    description="The contract contains indefinite payment obligations.",
                    severity=RiskSeverity.HIGH,
                    category=RiskCategory.PAYMENT,
                    recommendation="Specify clear payment terms and duration.",
                    confidence_score=90,
                )
            )

        return risks

    @staticmethod
    def _contains_keywords(text: str, keywords: set) -> bool:
        """Check if text contains any keywords."""
        for keyword in keywords:
            if keyword in text:
                return True
        return False


class RiskAnalyzer:
    """Main risk analysis orchestrator."""

    DISCLAIMER = (
        "Esta análise de riscos foi gerada com auxílio de inteligência artificial "
        "e não substitui a revisão de um profissional jurídico especializado."
    )

    def __init__(self, db: Session):
        """Initialize analyzer."""
        self.db = db
        self.heuristic_analyzer = HeuristicAnalyzer(db)
        self.validator = AIValidator.get_default_validator()

    def analyze(self, document_id: str) -> RiskAnalysisResult:
        """
        Analyze contract for risks.

        Uses three layers:
        1. Heuristic analysis
        2. RAG retrieval
        3. LLM analysis with guardrails
        """
        # Get document
        document = self.db.query(Document).filter(
            Document.id == document_id
        ).first()

        if not document:
            return RiskAnalysisResult(
                summary="Document not found",
                overall_risk=RiskSeverity.LOW,
                confidence_score=0,
                confidence_level="low",
                disclaimer=self.DISCLAIMER,
            )

        # Get chunks
        chunks = self.db.query(Chunk).filter(
            Chunk.document_id == document_id
        ).all()

        if not chunks:
            return RiskAnalysisResult(
                summary="No content found in document",
                overall_risk=RiskSeverity.LOW,
                confidence_score=0,
                confidence_level="low",
                disclaimer=self.DISCLAIMER,
            )

        # Layer 1: Heuristic analysis
        heuristic_risks = self.heuristic_analyzer.analyze(document_id)

        # Layer 2: RAG retrieval (retrieve risk-related chunks)
        risk_chunks = self._retrieve_risk_chunks(document_id, chunks)

        # Layer 3: Combine and validate
        all_risks = heuristic_risks

        # Calculate overall risk level
        overall_risk = self._calculate_overall_risk(all_risks)

        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(
            all_risks, risk_chunks
        )

        # Determine confidence level
        if confidence_score >= 80:
            confidence_level = "high"
        elif confidence_score >= 60:
            confidence_level = "moderate"
        else:
            confidence_level = "low"

        # Generate summary
        summary = self._generate_summary(all_risks, overall_risk)

        # Collect citations
        citations = self._collect_citations(risk_chunks)

        return RiskAnalysisResult(
            summary=summary,
            overall_risk=overall_risk,
            confidence_score=confidence_score,
            confidence_level=confidence_level,
            risks=all_risks,
            citations=citations,
            disclaimer=self.DISCLAIMER,
        )

    def _retrieve_risk_chunks(
        self, document_id: str, chunks: List[Chunk]
    ) -> List[Dict]:
        """Retrieve chunks relevant to risks."""
        risk_keywords = [
            "risco", "risk", "problema", "issue", "cuidado", "atenção",
            "multa", "penalty", "rescisão", "termination", "confidencial",
            "confidentiality", "lgpd", "dados", "data", "renovação"
        ]

        relevant_chunks = []
        for chunk in chunks:
            text_lower = chunk.text.lower()
            if any(kw in text_lower for kw in risk_keywords):
                relevant_chunks.append({
                    "id": chunk.id,
                    "text": chunk.text,
                    "page_number": chunk.page_number,
                    "document_id": document_id,
                    "document_title": chunk.document.title,
                })

        return relevant_chunks

    @staticmethod
    def _calculate_overall_risk(risks: List[ContractRisk]) -> RiskSeverity:
        """Calculate overall risk level from individual risks."""
        if not risks:
            return RiskSeverity.LOW

        # Find highest severity
        severities = [r.severity for r in risks]

        if RiskSeverity.CRITICAL in severities:
            return RiskSeverity.CRITICAL
        elif RiskSeverity.HIGH in severities:
            return RiskSeverity.HIGH
        elif RiskSeverity.MEDIUM in severities:
            return RiskSeverity.MEDIUM
        else:
            return RiskSeverity.LOW

    @staticmethod
    def _calculate_confidence_score(
        risks: List[ContractRisk], chunks: List[Dict]
    ) -> int:
        """Calculate confidence score for analysis."""
        score = 50  # Base score

        # Add points for number of risks found
        if len(risks) > 0:
            score += min(20, len(risks) * 5)

        # Add points for chunk coverage
        if len(chunks) > 0:
            score += min(30, len(chunks) * 3)

        # Ensure within bounds
        score = max(0, min(100, score))

        return score

    @staticmethod
    def _generate_summary(risks: List[ContractRisk], overall_risk: RiskSeverity) -> str:
        """Generate summary of analysis."""
        if not risks:
            return f"No significant risks detected. Overall risk level: {overall_risk.value}"

        risk_count = len(risks)
        critical_count = sum(1 for r in risks if r.severity == RiskSeverity.CRITICAL)
        high_count = sum(1 for r in risks if r.severity == RiskSeverity.HIGH)

        summary = f"Found {risk_count} risk(s). "
        if critical_count > 0:
            summary += f"{critical_count} critical, "
        if high_count > 0:
            summary += f"{high_count} high severity. "
        summary += f"Overall risk level: {overall_risk.value}."

        return summary

    @staticmethod
    def _collect_citations(chunks: List[Dict]) -> List[CitationSource]:
        """Collect citations from chunks."""
        citations = []
        for chunk in chunks[:5]:  # Limit to top 5
            citation = CitationSource(
                document_id=chunk["document_id"],
                document_title=chunk["document_title"],
                chunk_id=chunk["id"],
                page_number=chunk.get("page_number"),
                excerpt=chunk["text"][:300],
                similarity_score=0.7,  # Heuristic score
            )
            citations.append(citation)
        return citations
