from pydantic_settings import BaseSettings
from functools import lru_cache
import os
import sys


class Settings(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    secret_key: str = ""
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "legal_ai.log")
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # RAG Configuration
    rag_top_k: int = int(os.getenv("RAG_TOP_K", "5"))
    min_similarity_score: float = float(os.getenv("MIN_SIMILARITY_SCORE", "0.3"))
    
    # AI Validation thresholds
    min_confidence_score: int = int(os.getenv("MIN_CONFIDENCE_SCORE", "60"))
    min_citations: int = int(os.getenv("MIN_CITATIONS", "1"))
    max_citation_excerpt_length: int = int(os.getenv("MAX_CITATION_EXCERPT_LENGTH", "300"))
    
    # Automation / Webhook settings
    automation_webhook_url: str = os.getenv("AUTOMATION_WEBHOOK_URL", "")
    automation_webhook_timeout_seconds: int = int(os.getenv("AUTOMATION_WEBHOOK_TIMEOUT_SECONDS", "10"))
    automation_webhook_max_retries: int = int(os.getenv("AUTOMATION_WEBHOOK_MAX_RETRIES", "3"))
    automation_webhook_enabled: bool = os.getenv("AUTOMATION_WEBHOOK_ENABLED", "false").lower() == "true"
    
    # Estimated manual processing times (minutes) — illustrative MVP reference values
    estimated_manual_summary_minutes: int = int(os.getenv("ESTIMATED_MANUAL_SUMMARY_MINUTES", "30"))
    estimated_manual_extraction_minutes: int = int(os.getenv("ESTIMATED_MANUAL_EXTRACTION_MINUTES", "45"))
    estimated_manual_comparison_minutes: int = int(os.getenv("ESTIMATED_MANUAL_COMPARISON_MINUTES", "90"))
    estimated_manual_qa_minutes: int = int(os.getenv("ESTIMATED_MANUAL_QA_MINUTES", "15"))
    estimated_manual_risk_analysis_minutes: int = int(os.getenv("ESTIMATED_MANUAL_RISK_ANALYSIS_MINUTES", "120"))
    
    def __init__(self, **data):
        super().__init__(**data)
        self._validate_secret_key()
    
    def _validate_secret_key(self):
        """Validate SECRET_KEY configuration."""
        secret_key = os.getenv("SECRET_KEY", "").strip()
        
        # In production, SECRET_KEY must be set and secure
        if self.environment == "production":
            if not secret_key:
                raise ValueError(
                    "SECRET_KEY environment variable is required in production"
                )
            if secret_key == "your-secret-key-change-in-production":
                raise ValueError(
                    "SECRET_KEY must be changed from default value in production"
                )
            if len(secret_key) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters long in production"
                )
        
        # In development/testing, allow test key
        if self.environment in ("development", "testing"):
            if not secret_key:
                # Use a development key (not secure, only for development)
                secret_key = "dev-secret-key-do-not-use-in-production-" + "x" * 20
                print(
                    "⚠️  WARNING: Using development SECRET_KEY. "
                    "Set SECRET_KEY environment variable for production."
                )
        
        self.secret_key = secret_key
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
