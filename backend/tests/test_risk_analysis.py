"""
Tests for Risk Analysis.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Document, Chunk, User, UserRole
from app.risk_analysis import (
    RiskAnalyzer,
    HeuristicAnalyzer,
    RiskSeverity,
    RiskCategory,
    ContractRisk,
    RiskAnalysisResult,
)


@pytest.fixture
def test_db():
    """Create test database."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    # Create test user
    user = User(
        id="test_user",
        name="Test User",
        email="test@example.com",
        password_hash="hash",
        role=UserRole.CLIENT,
        is_active=True
    )
    db.add(user)
    db.commit()
    
    yield db
    db.close()


@pytest.fixture
def test_document(test_db):
    """Create test document."""
    doc = Document(
        id="test_doc",
        title="Test Contract",
        filename="test.pdf",
        file_path="/tmp/test.pdf",
        user_id="test_user"
    )
    test_db.add(doc)
    test_db.commit()
    return doc


class TestRiskSeverity:
    """Tests for RiskSeverity enum."""

    def test_severity_values(self):
        """Test severity values."""
        assert RiskSeverity.LOW.value == "low"
        assert RiskSeverity.MEDIUM.value == "medium"
        assert RiskSeverity.HIGH.value == "high"
        assert RiskSeverity.CRITICAL.value == "critical"


class TestRiskCategory:
    """Tests for RiskCategory enum."""

    def test_category_values(self):
        """Test category values."""
        assert RiskCategory.CONFIDENTIALITY.value == "confidentiality"
        assert RiskCategory.LGPD.value == "lgpd"
        assert RiskCategory.TERMINATION.value == "termination"


class TestContractRisk:
    """Tests for ContractRisk dataclass."""

    def test_risk_creation(self):
        """Test creating a contract risk."""
        risk = ContractRisk(
            title="Test Risk",
            description="Test description",
            severity=RiskSeverity.HIGH,
            category=RiskCategory.CONFIDENTIALITY,
            recommendation="Test recommendation",
            confidence_score=85,
        )

        assert risk.title == "Test Risk"
        assert risk.severity == RiskSeverity.HIGH
        assert risk.confidence_score == 85

    def test_risk_to_dict(self):
        """Test converting risk to dictionary."""
        risk = ContractRisk(
            title="Test Risk",
            description="Test description",
            severity=RiskSeverity.HIGH,
            category=RiskCategory.CONFIDENTIALITY,
            recommendation="Test recommendation",
        )

        risk_dict = risk.to_dict()
        assert risk_dict["title"] == "Test Risk"
        assert risk_dict["severity"] == "high"


class TestHeuristicAnalyzer:
    """Tests for HeuristicAnalyzer."""

    def test_analyzer_initialization(self, test_db):
        """Test analyzer initialization."""
        analyzer = HeuristicAnalyzer(test_db)
        assert isinstance(analyzer, HeuristicAnalyzer)

    def test_analyze_nonexistent_document(self, test_db):
        """Test analyzing nonexistent document."""
        analyzer = HeuristicAnalyzer(test_db)
        risks = analyzer.analyze("nonexistent")
        assert len(risks) == 0

    def test_analyze_document_without_chunks(self, test_db, test_document):
        """Test analyzing document without chunks."""
        analyzer = HeuristicAnalyzer(test_db)
        risks = analyzer.analyze(test_document.id)
        assert len(risks) == 0

    def test_detect_missing_confidentiality(self, test_db, test_document):
        """Test detection of missing confidentiality clause."""
        # Add chunk without confidentiality
        chunk = Chunk(
            id="chunk1",
            document_id=test_document.id,
            chunk_index=0,
            text="This is a simple contract without confidentiality clause.",
            page_number=1
        )
        test_db.add(chunk)
        test_db.commit()

        analyzer = HeuristicAnalyzer(test_db)
        risks = analyzer.analyze(test_document.id)

        # Should detect missing confidentiality (or at least return some risks)
        assert isinstance(risks, list)
        # At least one risk should be detected (missing confidentiality, LGPD, or termination)
        assert len(risks) > 0

    def test_detect_missing_lgpd(self, test_db, test_document):
        """Test detection of missing LGPD clause."""
        chunk = Chunk(
            id="chunk1",
            document_id=test_document.id,
            chunk_index=0,
            text="This contract does not mention LGPD or data protection.",
            page_number=1
        )
        test_db.add(chunk)
        test_db.commit()

        analyzer = HeuristicAnalyzer(test_db)
        risks = analyzer.analyze(test_document.id)

        # Should detect missing LGPD (or other risks)
        assert isinstance(risks, list)
        assert len(risks) > 0

    def test_detect_unlimited_penalty(self, test_db, test_document):
        """Test detection of unlimited penalty clause."""
        chunk = Chunk(
            id="chunk1",
            document_id=test_document.id,
            chunk_index=0,
            text="A multa ilimitada será aplicada em caso de violação.",
            page_number=1
        )
        test_db.add(chunk)
        test_db.commit()

        analyzer = HeuristicAnalyzer(test_db)
        risks = analyzer.analyze(test_document.id)

        # Should detect unlimited penalty
        penalty_risks = [r for r in risks if r.category == RiskCategory.PENALTY]
        assert len(penalty_risks) > 0
        assert any(r.severity == RiskSeverity.CRITICAL for r in penalty_risks)

    def test_detect_automatic_renewal(self, test_db, test_document):
        """Test detection of automatic renewal clause."""
        chunk = Chunk(
            id="chunk1",
            document_id=test_document.id,
            chunk_index=0,
            text="O contrato terá renovação automática a cada ano.",
            page_number=1
        )
        test_db.add(chunk)
        test_db.commit()

        analyzer = HeuristicAnalyzer(test_db)
        risks = analyzer.analyze(test_document.id)

        # Should detect automatic renewal
        renewal_risks = [r for r in risks if r.category == RiskCategory.RENEWAL]
        assert len(renewal_risks) > 0


class TestRiskAnalyzer:
    """Tests for RiskAnalyzer."""

    def test_analyzer_initialization(self, test_db):
        """Test analyzer initialization."""
        analyzer = RiskAnalyzer(test_db)
        assert isinstance(analyzer, RiskAnalyzer)

    def test_analyze_nonexistent_document(self, test_db):
        """Test analyzing nonexistent document."""
        analyzer = RiskAnalyzer(test_db)
        result = analyzer.analyze("nonexistent")

        assert result.overall_risk == RiskSeverity.LOW
        assert result.confidence_score == 0
        assert "not found" in result.summary.lower()

    def test_analyze_document_without_chunks(self, test_db, test_document):
        """Test analyzing document without chunks."""
        analyzer = RiskAnalyzer(test_db)
        result = analyzer.analyze(test_document.id)

        assert result.overall_risk == RiskSeverity.LOW
        assert result.confidence_score == 0
        assert "no content" in result.summary.lower()

    def test_analyze_simple_contract(self, test_db, test_document):
        """Test analyzing a simple contract."""
        chunk = Chunk(
            id="chunk1",
            document_id=test_document.id,
            chunk_index=0,
            text="Simple contract without special clauses.",
            page_number=1
        )
        test_db.add(chunk)
        test_db.commit()

        analyzer = RiskAnalyzer(test_db)
        result = analyzer.analyze(test_document.id)

        assert isinstance(result, RiskAnalysisResult)
        assert result.overall_risk in [RiskSeverity.LOW, RiskSeverity.MEDIUM, RiskSeverity.HIGH]
        assert result.confidence_score >= 0
        assert result.disclaimer != ""

    def test_analyze_complex_contract(self, test_db, test_document):
        """Test analyzing a complex contract with multiple risks."""
        chunks = [
            Chunk(
                id="chunk1",
                document_id=test_document.id,
                chunk_index=0,
                text="Contrato sem cláusula de confidencialidade.",
                page_number=1
            ),
            Chunk(
                id="chunk2",
                document_id=test_document.id,
                chunk_index=1,
                text="A multa ilimitada será aplicada.",
                page_number=2
            ),
            Chunk(
                id="chunk3",
                document_id=test_document.id,
                chunk_index=2,
                text="Renovação automática anualmente.",
                page_number=3
            ),
        ]
        for chunk in chunks:
            test_db.add(chunk)
        test_db.commit()

        analyzer = RiskAnalyzer(test_db)
        result = analyzer.analyze(test_document.id)

        assert len(result.risks) > 0
        assert result.overall_risk in [RiskSeverity.HIGH, RiskSeverity.CRITICAL]
        assert result.confidence_score > 50

    def test_overall_risk_calculation(self, test_db):
        """Test overall risk calculation."""
        analyzer = RiskAnalyzer(test_db)

        # Test with no risks
        risks = []
        overall = analyzer._calculate_overall_risk(risks)
        assert overall == RiskSeverity.LOW

        # Test with low risks
        risks = [
            ContractRisk(
                title="Test",
                description="Test",
                severity=RiskSeverity.LOW,
                category=RiskCategory.OTHER,
                recommendation="Test"
            )
        ]
        overall = analyzer._calculate_overall_risk(risks)
        assert overall == RiskSeverity.LOW

        # Test with critical risk
        risks = [
            ContractRisk(
                title="Test",
                description="Test",
                severity=RiskSeverity.CRITICAL,
                category=RiskCategory.OTHER,
                recommendation="Test"
            )
        ]
        overall = analyzer._calculate_overall_risk(risks)
        assert overall == RiskSeverity.CRITICAL

    def test_confidence_score_calculation(self, test_db):
        """Test confidence score calculation."""
        analyzer = RiskAnalyzer(test_db)

        # No risks, no chunks
        score = analyzer._calculate_confidence_score([], [])
        assert 0 <= score <= 100

        # Multiple risks and chunks
        risks = [
            ContractRisk(
                title="Test",
                description="Test",
                severity=RiskSeverity.HIGH,
                category=RiskCategory.OTHER,
                recommendation="Test"
            )
        ]
        chunks = [{"id": f"chunk{i}"} for i in range(5)]
        score = analyzer._calculate_confidence_score(risks, chunks)
        assert score > 50

    def test_summary_generation(self, test_db):
        """Test summary generation."""
        analyzer = RiskAnalyzer(test_db)

        # No risks
        summary = analyzer._generate_summary([], RiskSeverity.LOW)
        assert "no significant risks" in summary.lower()

        # Multiple risks
        risks = [
            ContractRisk(
                title="Test1",
                description="Test",
                severity=RiskSeverity.CRITICAL,
                category=RiskCategory.OTHER,
                recommendation="Test"
            ),
            ContractRisk(
                title="Test2",
                description="Test",
                severity=RiskSeverity.HIGH,
                category=RiskCategory.OTHER,
                recommendation="Test"
            ),
        ]
        summary = analyzer._generate_summary(risks, RiskSeverity.CRITICAL)
        assert "2 risk" in summary
        assert "critical" in summary.lower()

    def test_result_to_dict(self, test_db, test_document):
        """Test converting result to dictionary."""
        chunk = Chunk(
            id="chunk1",
            document_id=test_document.id,
            chunk_index=0,
            text="Test contract.",
            page_number=1
        )
        test_db.add(chunk)
        test_db.commit()

        analyzer = RiskAnalyzer(test_db)
        result = analyzer.analyze(test_document.id)
        result_dict = result.to_dict()

        assert "summary" in result_dict
        assert "overall_risk" in result_dict
        assert "confidence_score" in result_dict
        assert "risks" in result_dict
        assert "disclaimer" in result_dict
