"""
Tests for Automation service, endpoints, and webhook.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime

from app.main import app
from app.models import User, Document, Chunk, Conversation, AutomationRun, UserRole
from app.auth import create_access_token, hash_password
from app.automation_service import (
    create_automation_run,
    update_run_status,
    run_post_upload_automation,
)
from app.webhook_service import build_analysis_completed_payload, send_webhook
from tests.conftest import TestingSessionLocal

client = TestClient(app)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db):
    user = User(
        name="Test User",
        email="test_auto@example.com",
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
        name="Admin",
        email="admin_auto@example.com",
        password_hash=hash_password("adminpassword123"),
        role=UserRole.ADMIN,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_document(db, test_user):
    doc = Document(
        title="Test Contract",
        filename="test.pdf",
        file_path="/tmp/test.pdf",
        status="ready",
        user_id=test_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text="This is a test contract about payment.",
        page_number=1,
    )
    db.add(chunk)
    db.commit()
    return doc


@pytest.fixture
def auth_token(test_user):
    return create_access_token(data={"sub": test_user.id, "role": test_user.role.value})


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": admin_user.id, "role": admin_user.role.value})


class TestAutomationRunModel:
    """Test AutomationRun model and service functions."""

    def test_create_automation_run(self, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        assert run.id is not None
        assert run.status == "PENDING"
        assert run.current_step == "DOCUMENT_PROCESSING"
        assert run.progress_percent == 0
        assert run.webhook_status == "pending"

    def test_update_run_status(self, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        update_run_status(
            db, run.id,
            status="RUNNING",
            current_step="SUMMARY",
            progress_percent=30,
        )
        db.refresh(run)
        assert run.status == "RUNNING"
        assert run.current_step == "SUMMARY"
        assert run.progress_percent == 30
        assert run.started_at is not None

    def test_complete_run(self, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        update_run_status(
            db, run.id,
            status="COMPLETED",
            current_step="COMPLETED",
            progress_percent=100,
        )
        db.refresh(run)
        assert run.status == "COMPLETED"
        assert run.completed_at is not None

    def test_fail_run(self, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        update_run_status(
            db, run.id,
            status="FAILED",
            error_message="Something went wrong",
            progress_percent=100,
        )
        db.refresh(run)
        assert run.status == "FAILED"
        assert run.error_message == "Something went wrong"
        assert run.completed_at is not None


class TestAutomationEndpoints:
    """Test automation API endpoints."""

    def test_list_runs_user_sees_own(self, client, auth_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        response = client.get(
            "/automations/runs",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == run.id

    def test_list_runs_admin_sees_all(self, client, admin_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        response = client.get(
            "/automations/runs",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1

    def test_list_runs_filter_by_status(self, client, auth_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        update_run_status(db, run.id, status="COMPLETED", progress_percent=100)
        response = client.get(
            "/automations/runs?status=COMPLETED",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert all(r["status"] == "COMPLETED" for r in data)

    def test_get_run_by_id(self, client, auth_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        response = client.get(
            f"/automations/runs/{run.id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == run.id

    def test_get_run_not_found(self, client, auth_token):
        response = client.get(
            "/automations/runs/nonexistent-id",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 404

    def test_retry_failed_run(self, client, auth_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        update_run_status(db, run.id, status="FAILED", error_message="test error", progress_percent=100)

        with patch('app.main.run_post_upload_automation'):
            response = client.post(
                f"/automations/runs/{run.id}/retry",
                headers={"Authorization": f"Bearer {auth_token}"},
            )
        assert response.status_code == 200
        assert "Retry scheduled" in response.json()["message"]

    def test_retry_non_failed_run(self, client, auth_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        # Run is PENDING, should not be retryable
        response = client.post(
            f"/automations/runs/{run.id}/retry",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 400


class TestAutomationExecution:
    """Test the background automation execution."""

    def test_automation_creates_summary_and_risk(self, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)

        with patch('app.legal_agent.LegalAgent') as MockAgent:
            mock_agent = MagicMock()
            mock_summary_tool = MagicMock()
            mock_summary_tool._run.return_value = "Summary result"
            mock_agent.tools = [None, mock_summary_tool, None, None]
            MockAgent.return_value = mock_agent

            with patch('app.automation_service.send_webhook') as mock_webhook:
                mock_webhook.return_value = {"success": True, "status_code": 200, "error": None}

                with patch('app.automation_service.SessionLocal', TestingSessionLocal):
                    run_post_upload_automation(run.id, test_document.id, test_user.id)

        db.refresh(run)
        assert run.status == "COMPLETED"
        assert run.progress_percent == 100
        assert run.summary_result is not None
        assert run.risk_result is not None
        assert run.webhook_status == "sent"

    def test_automation_webhook_failure_does_not_destroy_results(self, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)

        with patch('app.legal_agent.LegalAgent') as MockAgent:
            mock_agent = MagicMock()
            mock_summary_tool = MagicMock()
            mock_summary_tool._run.return_value = "Summary result"
            mock_agent.tools = [None, mock_summary_tool, None, None]
            MockAgent.return_value = mock_agent

            with patch('app.automation_service.send_webhook') as mock_webhook:
                mock_webhook.return_value = {"success": False, "status_code": None, "error": "Connection refused"}

                with patch('app.automation_service.SessionLocal', TestingSessionLocal):
                    run_post_upload_automation(run.id, test_document.id, test_user.id)

        db.refresh(run)
        assert run.summary_result is not None
        assert run.risk_result is not None
        assert run.status == "PARTIAL_SUCCESS"
        assert run.webhook_status == "failed"
        assert run.webhook_error is not None

    def test_automation_failed_document_not_found(self, db, test_user):
        run = create_automation_run(db, "fake-doc-id", test_user.id)

        with patch('app.automation_service.SessionLocal', TestingSessionLocal):
            run_post_upload_automation(run.id, "fake-doc-id", test_user.id)

        db.refresh(run)
        assert run.status == "FAILED"
        assert "not found" in (run.error_message or "").lower()


class TestWebhook:
    """Test webhook payload and sending."""

    def test_payload_structure(self):
        payload = build_analysis_completed_payload(
            run_id="run-123",
            document_id="doc-456",
            document_title="Test Contract",
            status="COMPLETED",
            summary_available=True,
            risk_analysis_available=True,
            overall_risk="high",
            confidence_score=85,
        )
        assert payload["event"] == "analysis.completed"
        assert payload["event_id"]  # UUID
        assert payload["timestamp"]  # ISO-8601
        assert payload["document"]["id"] == "doc-456"
        assert payload["document"]["title"] == "Test Contract"
        assert payload["automation"]["run_id"] == "run-123"
        assert payload["automation"]["status"] == "COMPLETED"
        assert payload["analysis"]["summary_available"] is True
        assert payload["analysis"]["risk_analysis_available"] is True
        assert payload["analysis"]["overall_risk"] == "high"
        assert payload["analysis"]["confidence_score"] == 85

    def test_payload_no_sensitive_data(self):
        payload = build_analysis_completed_payload(
            run_id="run-123",
            document_id="doc-456",
            document_title="Test",
            status="COMPLETED",
            summary_available=True,
            risk_analysis_available=True,
        )
        payload_str = str(payload)
        assert "password" not in payload_str.lower()
        assert "token" not in payload_str.lower()
        assert "authorization" not in payload_str.lower()
        assert "api_key" not in payload_str.lower()
        assert "prompt" not in payload_str.lower()

    def test_webhook_disabled_does_not_send(self):
        with patch('app.webhook_service.get_settings') as mock_settings:
            mock_s = MagicMock()
            mock_s.automation_webhook_enabled = False
            mock_settings.return_value = mock_s

            result = send_webhook({"event": "test"}, "event-123")
            assert result["success"] is False
            assert "disabled" in result["error"].lower()

    def test_webhook_no_url_does_not_send(self):
        with patch('app.webhook_service.get_settings') as mock_settings:
            mock_s = MagicMock()
            mock_s.automation_webhook_enabled = True
            mock_s.automation_webhook_url = ""
            mock_settings.return_value = mock_s

            result = send_webhook({"event": "test"}, "event-123")
            assert result["success"] is False
            assert "url" in result["error"].lower()

    def test_webhook_timeout_handled(self):
        with patch('app.webhook_service.get_settings') as mock_settings:
            mock_s = MagicMock()
            mock_s.automation_webhook_enabled = True
            mock_s.automation_webhook_url = "http://example.com/webhook"
            mock_s.automation_webhook_timeout_seconds = 1
            mock_s.automation_webhook_max_retries = 2
            mock_settings.return_value = mock_s

            with patch('httpx.Client') as mock_client:
                mock_client_instance = MagicMock()
                mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
                mock_client_instance.__exit__ = MagicMock(return_value=False)
                import httpx
                mock_client_instance.post.side_effect = httpx.TimeoutException("timeout")
                mock_client.return_value = mock_client_instance

                result = send_webhook({"event": "test"}, "event-123")
                assert result["success"] is False
                assert "retries" in result["error"].lower()

    def test_webhook_idempotency_key_in_header(self):
        with patch('app.webhook_service.get_settings') as mock_settings:
            mock_s = MagicMock()
            mock_s.automation_webhook_enabled = True
            mock_s.automation_webhook_url = "http://example.com/webhook"
            mock_s.automation_webhook_timeout_seconds = 10
            mock_s.automation_webhook_max_retries = 1
            mock_settings.return_value = mock_s

            with patch('httpx.Client') as mock_client:
                mock_client_instance = MagicMock()
                mock_client_instance.__enter__ = MagicMock(return_value=mock_client_instance)
                mock_client_instance.__exit__ = MagicMock(return_value=False)
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_client_instance.post.return_value = mock_response
                mock_client.return_value = mock_client_instance

                send_webhook({"event": "test"}, "event-id-456")

                # Check idempotency key header
                call_args = mock_client_instance.post.call_args
                headers = call_args.kwargs.get("headers", {})
                assert headers.get("X-Idempotency-Key") == "event-id-456"
                assert headers.get("Content-Type") == "application/json"


class TestSystemStatus:
    """Test admin system status endpoint."""

    def test_system_status_admin_only(self, client, auth_token):
        response = client.get(
            "/admin/system-status",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
        assert response.status_code == 403

    def test_system_status_returns_data(self, client, admin_token, db, test_document, test_user):
        run = create_automation_run(db, test_document.id, test_user.id)
        update_run_status(db, run.id, status="COMPLETED", progress_percent=100)

        response = client.get(
            "/admin/system-status",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data
        assert "automation_runs_by_status" in data
        assert "total_documents" in data
        assert "total_risk_analyses" in data
        assert "recent_failures" in data
        assert "failed_webhooks" in data
