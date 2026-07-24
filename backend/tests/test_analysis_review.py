"""
Tests for Analysis Records, Reviews, and Impact Metrics.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.models import User, UserRole, Document, AnalysisRecord, AnalysisReview
from app.auth import create_access_token, hash_password
from app.analysis_record_service import (
    create_analysis_record,
    create_review,
    validate_transition,
    DECISION_TO_STATUS,
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
        name="Test Lawyer",
        email="test@lawyer.com",
        password_hash=hash_password("testpassword123"),
        role=UserRole.LAWYER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_user(db):
    user = User(
        name="Test Admin",
        email="test@admin.com",
        password_hash=hash_password("adminpassword123"),
        role=UserRole.ADMIN,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def assistant_user(db):
    user = User(
        name="Test Assistant",
        email="test@assistant.com",
        password_hash=hash_password("asstpassword123"),
        role=UserRole.ASSISTANT,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(lawyer_user):
    return create_access_token(data={"sub": lawyer_user.id, "role": lawyer_user.role.value})


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": admin_user.id, "role": admin_user.role.value})


@pytest.fixture
def assistant_token(assistant_user):
    return create_access_token(data={"sub": assistant_user.id, "role": assistant_user.role.value})


@pytest.fixture
def test_document(db, lawyer_user):
    doc = Document(
        title="Test Contract",
        filename="test.pdf",
        file_path="/tmp/test.pdf",
        status="ready",
        page_count=5,
        user_id=lawyer_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


class TestAnalysisRecordModel:
    """Test AnalysisRecord creation and fields."""

    def test_create_analysis_record(self, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="This is a test summary.",
            model_name="heuristic",
        )
        assert record.id is not None
        assert record.analysis_type == "SUMMARY"
        assert record.status == "GENERATED"
        assert record.version == 1
        assert record.estimated_manual_minutes > 0
        assert record.estimated_time_saved_minutes > 0
        assert record.prompt_version is not None

    def test_analysis_record_with_structured_data(self, db, lawyer_user, test_document):
        structured = {
            "overall_risk": "medium",
            "risks": [
                {"title": "Risk 1", "severity": "high"},
                {"title": "Risk 2", "severity": "low"},
            ],
        }
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_RISK_ANALYSIS,
            content_summary="Risk analysis summary",
            structured_result=structured,
            confidence_score=75,
            confidence_level="medium",
            overall_risk="medium",
            model_name="heuristic",
        )
        assert record.structured_result == structured
        assert record.confidence_score == 75
        assert record.overall_risk == "medium"


class TestStateTransitions:
    """Test analysis status state machine."""

    def test_generated_to_pending_review(self):
        assert validate_transition("GENERATED", "PENDING_REVIEW") is True

    def test_generated_to_approved_invalid(self):
        assert validate_transition("GENERATED", "APPROVED") is False

    def test_pending_review_to_approved(self):
        assert validate_transition("PENDING_REVIEW", "APPROVED") is True

    def test_pending_review_to_rejected(self):
        assert validate_transition("PENDING_REVIEW", "REJECTED") is True

    def test_approved_is_terminal(self):
        assert validate_transition("APPROVED", "PENDING_REVIEW") is False
        assert validate_transition("APPROVED", "REJECTED") is False

    def test_needs_changes_to_pending_review(self):
        assert validate_transition("NEEDS_CHANGES", "PENDING_REVIEW") is True

    def test_rejected_to_pending_review(self):
        assert validate_transition("REJECTED", "PENDING_REVIEW") is True


class TestReviewEndpoints:
    """Test analysis review API endpoints."""

    def test_list_analyses(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Test summary",
            model_name="heuristic",
        )
        response = client.get(
            "/analyses",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["analysis_type"] == "SUMMARY"

    def test_get_analysis_detail(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Detail test",
            model_name="heuristic",
        )
        response = client.get(
            f"/analyses/{record.id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == record.id
        assert data["analysis_type"] == "SUMMARY"
        assert data["reviews"] == []

    def test_create_review_approve(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Approve test",
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        response = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "APPROVE", "comment": "Looks good"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["decision"] == "APPROVE"
        assert data["new_status"] == "APPROVED"
        assert data["previous_status"] == "PENDING_REVIEW"

    def test_create_review_reject_requires_comment(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Reject test",
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        response = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "REJECT"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 400

    def test_create_review_reject_with_comment(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Reject with comment",
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        response = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "REJECT", "comment": "Missing key clauses"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 201
        assert response.json()["new_status"] == "REJECTED"

    def test_review_history(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="History test",
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "APPROVE", "comment": "Approved"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        response = client.get(
            f"/analyses/{record.id}/reviews",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["decision"] == "APPROVE"

    def test_invalid_transition(self, auth_token, db, lawyer_user, test_document):
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Invalid transition",
            model_name="heuristic",
        )

        response = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "APPROVE"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 400

    def test_404_nonexistent_analysis(self, auth_token):
        response = client.get(
            "/analyses/nonexistent-id",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 404

    def test_unauthenticated_list(self):
        response = client.get("/analyses")
        assert response.status_code == 401

    def test_request_changes_flow(self, auth_token, db, lawyer_user, test_document):
        """Full flow: PENDING_REVIEW -> REQUEST_CHANGES -> PENDING_REVIEW -> APPROVE."""
        record = create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Full flow test",
            model_name="heuristic",
        )
        record.status = "PENDING_REVIEW"
        db.commit()

        # Request changes
        resp = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "REQUEST_CHANGES", "comment": "Add more detail"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert resp.status_code == 201
        assert resp.json()["new_status"] == "NEEDS_CHANGES"

        # Back to pending review
        db.refresh(record)
        record.status = "PENDING_REVIEW"
        db.commit()

        # Approve
        resp = client.post(
            f"/analyses/{record.id}/reviews",
            json={"decision": "APPROVE", "comment": "Fixed"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert resp.status_code == 201
        assert resp.json()["new_status"] == "APPROVED"

        # Check history has 2 entries
        resp = client.get(
            f"/analyses/{record.id}/reviews",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert len(resp.json()) == 2


class TestMetricsEndpoint:
    """Test impact metrics endpoint."""

    def test_metrics_returns_data(self, auth_token, db, lawyer_user, test_document):
        create_analysis_record(
            db=db,
            document_id=test_document.id,
            user_id=lawyer_user.id,
            analysis_type=ANALYSIS_TYPE_SUMMARY,
            content_summary="Metrics test",
            model_name="heuristic",
        )
        response = client.get(
            "/metrics/impact",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "analyses_total" in data
        assert "estimation_notice" in data
        assert data["analyses_total"] >= 1
        assert "SUMMARY" in data["analyses_by_type"]

    def test_metrics_unauthenticated(self):
        response = client.get("/metrics/impact")
        assert response.status_code == 401


class TestSystemStatusEnhanced:
    """Test enhanced system status endpoint."""

    def test_system_status_has_new_fields(self, admin_token):
        response = client.get(
            "/admin/system-status",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "blocked_analyses" in data
        assert "pending_review" in data
        assert "health" in data
