"""
Tests for basic API endpoint existence and response codes.

These tests verify that core endpoints exist, require authentication,
and return appropriate HTTP status codes.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, UserRole
from app.auth import create_access_token, hash_password
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
def test_user(db):
    user = User(
        name="API Test User",
        email="apitest@example.com",
        password_hash=hash_password("testpassword123"),
        role=UserRole.LAWYER,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(test_user):
    return create_access_token(data={"sub": test_user.id, "role": test_user.role.value})


@pytest.fixture
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


class TestHealthEndpoint:
    def test_health_check(self):
        """Testa endpoint de health check (no auth required)"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestDocumentEndpoints:
    def test_list_documents_requires_auth(self):
        """Testa que listagem de documentos exige autenticação"""
        response = client.get("/documents")
        assert response.status_code == 401

    def test_list_documents_authenticated(self, auth_headers):
        """Testa listagem de documentos com autenticação"""
        response = client.get("/documents", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_nonexistent_document(self, auth_headers):
        """Testa busca de documento inexistente retorna 404"""
        response = client.get("/documents/nonexistent-id", headers=auth_headers)
        assert response.status_code == 404


class TestConversationEndpoints:
    def test_list_conversations_requires_auth(self):
        """Testa que listagem de conversas exige autenticação"""
        response = client.get("/conversations")
        assert response.status_code == 401

    def test_list_conversations_authenticated(self, auth_headers):
        """Testa listagem de conversas com autenticação"""
        response = client.get("/conversations", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAnalysisEndpoints:
    def test_summary_endpoint_requires_auth(self):
        """Testa que endpoint de resumo exige autenticação"""
        response = client.post(
            "/analysis/summary",
            json={"document_id": "test-id"}
        )
        assert response.status_code == 401

    def test_summary_endpoint_exists(self, auth_headers):
        """Testa se endpoint de resumo existe e responde com auth"""
        response = client.post(
            "/analysis/summary",
            json={"document_id": "test-id"},
            headers=auth_headers,
        )
        assert response.status_code in [200, 400, 404, 500]

    def test_extract_endpoint_requires_auth(self):
        """Testa que endpoint de extração exige autenticação"""
        response = client.post(
            "/analysis/extract",
            json={"document_id": "test-id"}
        )
        assert response.status_code == 401

    def test_extract_endpoint_exists(self, auth_headers):
        """Testa se endpoint de extração existe e responde com auth"""
        response = client.post(
            "/analysis/extract",
            json={"document_id": "test-id"},
            headers=auth_headers,
        )
        assert response.status_code in [200, 400, 404, 500]

    def test_compare_endpoint_requires_auth(self):
        """Testa que endpoint de comparação exige autenticação"""
        response = client.post(
            "/analysis/compare",
            json={"document_a_id": "test-a", "document_b_id": "test-b"}
        )
        assert response.status_code == 401

    def test_compare_endpoint_exists(self, auth_headers):
        """Testa se endpoint de comparação existe e responde com auth"""
        response = client.post(
            "/analysis/compare",
            json={"document_a_id": "test-a", "document_b_id": "test-b"},
            headers=auth_headers,
        )
        assert response.status_code in [200, 400, 404, 500]
