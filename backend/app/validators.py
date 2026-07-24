from typing import Any, Dict, List
import re


class ResponseValidator:
    """Valida respostas do modelo para detectar alucinações e erros"""
    
    @staticmethod
    def validate_extraction(data: Dict[str, List[str]]) -> Dict[str, Any]:
        """Valida dados extraídos"""
        errors = []
        warnings = []
        
        if not isinstance(data, dict):
            errors.append("Response is not a dictionary")
            return {"valid": False, "errors": errors, "warnings": warnings}
        
        required_fields = ["parties", "dates", "values", "clauses"]
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing field: {field}")
            elif not isinstance(data[field], list):
                errors.append(f"Field {field} must be a list")
        
        if "parties" in data and isinstance(data["parties"], list) and len(data["parties"]) == 0:
            warnings.append("No parties identified - may indicate extraction failure")
        
        if "dates" in data and isinstance(data["dates"], list) and len(data["dates"]) == 0:
            warnings.append("No dates identified - may indicate extraction failure")
        
        if "values" in data and isinstance(data["values"], list) and len(data["values"]) == 0:
            warnings.append("No values identified - may indicate extraction failure")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "data": data
        }
    
    @staticmethod
    def validate_summary(summary: str) -> Dict[str, Any]:
        """Valida resumo gerado"""
        errors = []
        warnings = []
        
        if not summary or len(summary.strip()) == 0:
            errors.append("Summary is empty")
        
        if len(summary) < 10:
            errors.append("Summary is too short to be meaningful")
        elif len(summary) < 50:
            warnings.append("Summary is too short - may be incomplete")
        
        if len(summary) > 5000:
            warnings.append("Summary is very long - may contain redundant information")
        
        if summary.count("não") > 5 or summary.count("não sei") > 2:
            warnings.append("Summary contains many negations - may indicate uncertainty")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "data": summary
        }
    
    @staticmethod
    def validate_chat_response(response: str, context: str = "") -> Dict[str, Any]:
        """Valida resposta do chat"""
        errors = []
        warnings = []
        
        if not response or len(response.strip()) == 0:
            errors.append("Response is empty")
        
        if len(response) < 10:
            errors.append("Response is too short")
        
        if "não sei" in response.lower() and not context:
            warnings.append("Response indicates uncertainty - no context provided")
        
        if "alucinação" in response.lower() or "inventado" in response.lower():
            warnings.append("Response may contain self-aware hallucination detection")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "data": response
        }
    
    @staticmethod
    def validate_confidence(response: str, min_confidence: float = 0.7) -> Dict[str, Any]:
        """Valida confiança da resposta"""
        confidence_indicators = {
            "certeza": 0.9,
            "definitivamente": 0.9,
            "claramente": 0.85,
            "provavelmente": 0.7,
            "possivelmente": 0.6,
            "talvez": 0.5,
            "incerto": 0.3,
            "não sei": 0.1,
        }
        
        response_lower = response.lower()
        matched_scores = []
        for indicator, score in confidence_indicators.items():
            if indicator.lower() in response_lower:
                matched_scores.append(score)

        if matched_scores:
            confidence_score = min(matched_scores)
        else:
            confidence_score = 0.5

        is_confident = confidence_score >= min_confidence
        
        return {
            "valid": is_confident,
            "confidence_score": confidence_score,
            "min_confidence": min_confidence,
            "message": "Response confidence is acceptable" if is_confident else "Response confidence is too low"
        }
