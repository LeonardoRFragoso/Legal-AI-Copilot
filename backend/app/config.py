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
