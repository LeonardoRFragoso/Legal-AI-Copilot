"""
Smoke test for the complete demo flow.

Tests the full workflow with external services mocked:
1. Create LAWYER user
2. Authenticate
3. Create document with chunks
4. Run summary analysis
5. Run risk analysis
6. Verify AnalysisRecord persistence
7. List analyses
8. Approve an analysis
9. Query review history
10. Query impact metrics

No real OpenAI calls. No real webhooks. No external dependencies.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.models import User, UserRole, Document, Chunk
from app.auth import create_access_token, hash_password
from app.analysis_record_service import (
    create_analysis_record,
    ANALYSIS_TYPE_SUMMARY,
    ANALYSIS_TYPE_RISK_ANALYSIS,
)
from tests.conftest import TestingSessionLocal

client = TestClient(app)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def lawyer_user(db):
    user = User(
        name="Smoke Test Lawyer",
        email="smoke@lawyer.com",
        password_hash=hash_password("smokepassword123"),
        role=UserRole.LAWYER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(lawyer_user):
    return create_access_token(data={"sub": lawyer_user.id, "role": lawyer_user.role.value})


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_document(db, lawyer_user):
    """Create a document with chunks mimicking the synthetic contract."""
    doc = Document(
        title="Contrato de Prestação de Serviços (Sintético)",
        filename="synthetic_contract.txt",
        file_path="/tmp/synthetic_contract.txt",
        status="ready",
        page_count=1,
        user_id=lawyer_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text=(
            "CONTRATO DE PRESTAÇÃO DE SERVIÇOS. "
            "CONTRATANTE: Empresa Fictícia LTDA. "
            "CONTRATADA: Tech Fictícia Solutions S.A. "
            "CLÁUSULA 4ª — MULTA: multa ilimitada, sem teto máximo. "
            "CLÁUSULA 5ª — RENOVAÇÃO AUTOMÁTICA: renovado automaticamente. "
            "CLÁUSULA 6ª — PAGAMENTO INDEFINIDO: pagamentos indefinidamente. "
            "CLÁUSULA 7ª — FORO: foro da Comarca da Cidade Fictícia. "
            "Não contém cláusula de confidencialidade. "
            "Não contém cláusula de LGPD."
        ),
        page_number=1,
    )
    db.add(chunk)
    db.commit()

    return doc


class TestDemoSmoke:
    """End-to-end smoke test of the demo flow."""

    def test_full_demo_flow(self, db, lawyer_user, auth_headers, test_document):
        """
        Complete demo flow:
        1. Auth works
        2. Documents accessible
        3. Summary analysis creates AnalysisRecord
        4. Risk analysis creates AnalysisRecord
        5. Analyses listed
        6. Review submitted
        7. Review history queried
        8. Metrics returned
        """

        # Step 1: Verify auth — access dashboard
        response = client.get("/documents", headers=auth_headers)
        assert response.status_code == 200
        docs = response.json()
        assert any(d["id"] == test_document.id for d in docs)

        # Step 2: Create summary AnalysisRecord (simulating chat/endpoint)
        summary_record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Resumo do contrato de prestação de serviços entre Empresa Fictícia e Tech Fictícia.",
            model_name="heuristic",
        )
        assert summary_record.id is not None
        assert summary_record.status == "GENERATED"

        # Step 3: Create risk analysis AnalysisRecord with structured data
        risk_record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_RISK_ANALYSIS,
            content_summary="Análise de riscos identificou 5 riscos.",
            structured_result={
                "overall_risk": "critical",
                "risks": [
                    {"title": "Unlimited Penalty Clause", "severity": "critical"},
                    {"title": "Missing Confidentiality Clause", "severity": "medium"},
                    {"title": "Missing LGPD Compliance Clause", "severity": "high"},
                    {"title": "Automatic Renewal Clause", "severity": "medium"},
                    {"title": "Indefinite Payment Obligation", "severity": "high"},
                ],
            },
            confidence_score=85,
            confidence_level="high",
            overall_risk="critical",
            model_name="heuristic",
        )
        assert risk_record.id is not None
        assert risk_record.overall_risk == "critical"

        # Step 4: List analyses
        response = client.get("/analyses", headers=auth_headers)
        assert response.status_code == 200
        analyses = response.json()
        assert len(analyses) >= 2

        # Step 5: Get analysis detail
        response = client.get(
            f"/analyses/{risk_record.id}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        detail = response.json()
        assert detail["analysis_type"] == "RISK_ANALYSIS"
        assert detail["overall_risk"] == "critical"
        assert len(detail["reviews"]) == 0

        # Step 6: Move to PENDING_REVIEW and approve
        risk_record.status = "PENDING_REVIEW"
        db.commit()

        response = client.post(
            f"/analyses/{risk_record.id}/reviews",
            json={"decision": "APPROVE", "comment": "Riscos identificados corretamente"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        review_data = response.json()
        assert review_data["decision"] == "APPROVE"
        assert review_data["new_status"] == "APPROVED"

        # Step 7: Query review history
        response = client.get(
            f"/analyses/{risk_record.id}/reviews",
            headers=auth_headers,
        )
        assert response.status_code == 200
        reviews = response.json()
        assert len(reviews) == 1
        assert reviews[0]["decision"] == "APPROVE"

        # Step 8: Query metrics
        response = client.get("/metrics/impact", headers=auth_headers)
        assert response.status_code == 200
        metrics = response.json()
        assert metrics["analyses_total"] >= 2
        assert "SUMMARY" in metrics["analyses_by_type"]
        assert "RISK_ANALYSIS" in metrics["analyses_by_type"]
        assert metrics["approval_rate"] > 0
        assert "estimation_notice" in metrics
        assert "critical" in metrics.get("risks_by_severity", {})

    def test_blocked_analysis_cannot_be_approved(self, db, lawyer_user, auth_headers, test_document):
        """Blocked analysis cannot be approved — guardrail enforcement."""
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Blocked analysis test",
            blocked=True,
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        response = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "APPROVE", "comment": "Trying to approve blocked"},
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert "blocked" in response.json()["detail"].lower()

    def test_rbac_assistant_cannot_review(self, db, lawyer_user, auth_headers, test_document):
        """ASSISTANT role cannot submit reviews."""
        # Create assistant user
        assistant = User(
            name="Smoke Assistant",
            email="smoke@assistant.com",
            password_hash=hash_password("assistantpassword123"),
            role=UserRole.ASSISTANT,
        )
        db.add(assistant)
        db.commit()
        db.refresh(assistant)
        assistant_token = create_access_token(
            data={"sub": assistant.id, "role": assistant.role.value}
        )

        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="RBAC test",
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        response = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "APPROVE", "comment": "Assistant trying to review"},
            headers={"Authorization": f"Bearer {assistant_token}"},
        )
        assert response.status_code == 403
