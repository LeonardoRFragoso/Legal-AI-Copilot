import pytest
from app.validators import ResponseValidator


class TestExtractionValidator:
    def test_valid_extraction(self):
        """Testa validação de extração válida"""
        data = {
            "parties": ["Party A", "Party B"],
            "dates": ["2026-01-01"],
            "values": ["R$ 1000"],
            "clauses": ["Confidentiality"]
        }
        result = ResponseValidator.validate_extraction(data)
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_missing_fields(self):
        """Testa validação com campos faltando"""
        data = {
            "parties": ["Party A"],
            "dates": []
        }
        result = ResponseValidator.validate_extraction(data)
        assert result["valid"] is False
        assert len(result["errors"]) > 0
    
    def test_empty_extraction(self):
        """Testa validação com extração vazia"""
        data = {
            "parties": [],
            "dates": [],
            "values": [],
            "clauses": []
        }
        result = ResponseValidator.validate_extraction(data)
        assert result["valid"] is True
        assert len(result["warnings"]) > 0


class TestSummaryValidator:
    def test_valid_summary(self):
        """Testa validação de resumo válido"""
        summary = "Este é um resumo válido com conteúdo suficiente para ser considerado completo."
        result = ResponseValidator.validate_summary(summary)
        assert result["valid"] is True
    
    def test_empty_summary(self):
        """Testa validação de resumo vazio"""
        summary = ""
        result = ResponseValidator.validate_summary(summary)
        assert result["valid"] is False
    
    def test_short_summary(self):
        """Testa validação de resumo muito curto"""
        summary = "Curto"
        result = ResponseValidator.validate_summary(summary)
        assert result["valid"] is False


class TestChatResponseValidator:
    def test_valid_response(self):
        """Testa validação de resposta válida"""
        response = "Esta é uma resposta completa e informativa sobre o documento."
        result = ResponseValidator.validate_chat_response(response)
        assert result["valid"] is True
    
    def test_empty_response(self):
        """Testa validação de resposta vazia"""
        response = ""
        result = ResponseValidator.validate_chat_response(response)
        assert result["valid"] is False
    
    def test_uncertain_response(self):
        """Testa validação de resposta incerta"""
        response = "Não sei responder essa pergunta"
        result = ResponseValidator.validate_chat_response(response)
        assert len(result["warnings"]) > 0


class TestConfidenceValidator:
    def test_confident_response(self):
        """Testa validação de resposta confiante"""
        response = "Definitivamente, este é o resultado correto."
        result = ResponseValidator.validate_confidence(response)
        assert result["valid"] is True
        assert result["confidence_score"] >= 0.7
    
    def test_uncertain_response(self):
        """Testa validação de resposta incerta"""
        response = "Talvez seja assim, mas não tenho certeza."
        result = ResponseValidator.validate_confidence(response)
        assert result["valid"] is False
        assert result["confidence_score"] < 0.7
    
    def test_low_confidence_response(self):
        """Testa validação de resposta com baixa confiança"""
        response = "Não sei ao certo."
        result = ResponseValidator.validate_confidence(response)
        assert result["valid"] is False
        assert result["confidence_score"] < 0.3
