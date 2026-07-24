"""
Tests for Agent Chat Integration.

Tests that the Agent Router is properly integrated into the chat flow,
correctly classifies intents, executes tools, and respects ownership/RBAC.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app.database import get_db
from app.models import User, Document, Conversation, Chunk, UserRole
from app.auth import create_access_token, hash_password
from app.agent_router import AgentIntent, LegalAgentRouter, RouterDecision
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
        email="test@example.com",
        password_hash=hash_password("testpassword123"),
        role=UserRole.LAWYER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def other_user(db):
    user = User(
        name="Other User",
        email="other@example.com",
        password_hash=hash_password("otherpassword123"),
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
        email="admin@example.com",
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
        text="This is a test contract clause about payment terms.",
        page_number=1,
    )
    db.add(chunk)
    db.commit()
    return doc


@pytest.fixture
def other_document(db, other_user):
    doc = Document(
        title="Other Contract",
        filename="other.pdf",
        file_path="/tmp/other.pdf",
        status="ready",
        user_id=other_user.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    chunk = Chunk(
        document_id=doc.id,
        chunk_index=0,
        text="Other contract content.",
        page_number=1,
    )
    db.add(chunk)
    db.commit()
    return doc


@pytest.fixture
def auth_token(test_user):
    return create_access_token(data={"sub": test_user.id, "role": test_user.role.value})


@pytest.fixture
def other_token(other_user):
    return create_access_token(data={"sub": other_user.id, "role": other_user.role.value})


@pytest.fixture
def admin_token(admin_user):
    return create_access_token(data={"sub": admin_user.id, "role": admin_user.role.value})


@pytest.fixture
def test_conversation(db, test_user, test_document):
    conv = Conversation(
        user_id=test_user.id,
        document_id=test_document.id,
        title="Test Conversation",
    )
    db.add(conv)
    db.commit()
    db.refresh(conv)
    return conv


class TestAgentRouterIntegration:
    """Test that the Agent Router correctly classifies chat messages."""

    def test_summarize_intent_via_chat(self, client, auth_token, test_conversation):
        """Summarize request selects SUMMARIZE_DOCUMENT."""
        with patch('app.main.legal_agent') as mock_agent:
            mock_tool = MagicMock()
            mock_tool._run.return_value = "This is a summary."
            mock_agent.tools = [None, mock_tool, None, None]

            response = client.post(
                f"/conversations/{test_conversation.id}/messages",
                json={"content": "faça um resumo do documento"},
                headers={"Authorization": f"Bearer {auth_token}"},
            )

        assert response.status_code == 200
        data = response.json()
        citations = data.get("citations", {})
        assert citations.get("agent", {}).get("intent") == "summarize_document"

    def test_extract_intent_via_chat(self, client, auth_token, test_conversation):
        """Extract request selects EXTRACT_INFORMATION."""
        with patch('app.main.legal_agent') as mock_agent:
            mock_tool = MagicMock()
            mock_tool._run.return_value = '{"parties": [], "dates": [], "values": [], "clauses": []}'
            mock_agent.tools = [None, None, mock_tool, None]

            response = client.post(
                f"/conversations/{test_conversation.id}/messages",
                json={"content": "extraia as partes do contrato"},
                headers={"Authorization": f"Bearer {auth_token}"},
            )

        assert response.status_code == 200
        data = response.json()
        citations = data.get("citations", {})
        assert citations.get("agent", {}).get("intent") == "extract_information"

    def test_risk_intent_via_chat(self, client, auth_token, test_conversation):
        """Risk question selects IDENTIFY_RISKS."""
        response = client.post(
            f"/conversations/{test_conversation.id}/messages",
            json={"content": "quais riscos existem neste contrato?"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        citations = data.get("citations", {})
        assert citations.get("agent", {}).get("intent") == "identify_risks"

    def test_question_answering_via_chat(self, client, auth_token, test_conversation):
        """Question selects QUESTION_ANSWERING."""
        with patch('app.main.legal_agent') as mock_agent:
            mock_agent.query.return_value = {"response": "Answer", "citations": []}

            response = client.post(
                f"/conversations/{test_conversation.id}/messages",
                json={"content": "qual é o valor do contrato?"},
                headers={"Authorization": f"Bearer {auth_token}"},
            )

        assert response.status_code == 200
        data = response.json()
        citations = data.get("citations", {})
        assert citations.get("agent", {}).get("intent") == "question_answering"

    def test_unknown_intent_via_chat(self, client, auth_token, test_conversation):
        """Unknown intent doesn't execute a tool."""
        response = client.post(
            f"/conversations/{test_conversation.id}/messages",
            json={"content": "xyz abc def random text"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        citations = data.get("citations", {})
        assert citations.get("agent", {}).get("intent") == "unknown"

    def test_document_of_other_user_returns_403(
        self, client, other_token, test_conversation
    ):
        """Cannot access conversation of another user."""
        response = client.post(
            f"/conversations/{test_conversation.id}/messages",
            json={"content": "faça um resumo"},
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert response.status_code == 403

    def test_router_decision_no_chain_of_thought(self):
        """RouterDecision does not expose chain of thought."""
        router = LegalAgentRouter()
        decision = router.route("faça um resumo", ["doc1"])
        # reason should be short and safe
        assert len(decision.reason) < 100
        assert "chain" not in decision.reason.lower()
        assert "thought" not in decision.reason.lower()

    def test_blocked_content_not_exposed(self, client, auth_token, test_conversation):
        """Content blocked by guardrails is not exposed."""
        from dataclasses import dataclass
        from typing import List

        @dataclass
        class FakeValidation:
            confidence_score: int = 10
            confidence_level: str = "low"
            hallucination_risk: str = "high"
            citations: list = None
            disclaimer: str = "Disclaimer"

        @dataclass
        class FakeResult:
            content: str = "A" * 10000
            blocked: bool = True
            block_reason: str = "Response blocked: excessive length without citations"
            validation: any = None

        fake_validation = FakeValidation(citations=[])
        fake_result = FakeResult(validation=fake_validation)

        with patch('app.main.legal_agent') as mock_agent:
            mock_agent.query.return_value = {"response": "A" * 10000, "citations": []}

            with patch('app.agent_executor.AIValidator') as MockValidator:
                MockValidator.get_default_validator.return_value.validate.return_value = fake_result

                response = client.post(
                    f"/conversations/{test_conversation.id}/messages",
                    json={"content": "qual é o valor?"},
                    headers={"Authorization": f"Bearer {auth_token}"},
                )

        assert response.status_code == 200
        data = response.json()
        assert "blocked" in data["content"].lower()
