import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health_check(self):
        """Testa endpoint de health check"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestDocumentEndpoints:
    def test_list_documents(self):
        """Testa listagem de documentos"""
        response = client.get("/documents")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_nonexistent_document(self):
        """Testa busca de documento inexistente"""
        response = client.get("/documents/nonexistent-id")
        assert response.status_code == 404 or response.status_code == 500


class TestConversationEndpoints:
    def test_list_conversations(self):
        """Testa listagem de conversas"""
        response = client.get("/conversations")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestAnalysisEndpoints:
    def test_summary_endpoint_exists(self):
        """Testa se endpoint de resumo existe"""
        response = client.post(
            "/analysis/summary",
            json={"document_id": "test-id"}
        )
        assert response.status_code in [200, 400, 500]
    
    def test_extract_endpoint_exists(self):
        """Testa se endpoint de extração existe"""
        response = client.post(
            "/analysis/extract",
            json={"document_id": "test-id"}
        )
        assert response.status_code in [200, 400, 500]
    
    def test_compare_endpoint_exists(self):
        """Testa se endpoint de comparação existe"""
        response = client.post(
            "/analysis/compare",
            json={"document_a_id": "test-a", "document_b_id": "test-b"}
        )
        assert response.status_code in [200, 400, 500]
