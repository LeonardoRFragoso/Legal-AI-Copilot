"""
Tests for configuration validation.
"""

import os
import pytest
from app.config import Settings


def test_production_requires_secret_key():
    """Test that production environment requires SECRET_KEY."""
    os.environ["ENVIRONMENT"] = "production"
    os.environ.pop("SECRET_KEY", None)
    
    with pytest.raises(ValueError, match="SECRET_KEY environment variable is required"):
        Settings()
    
    os.environ.pop("ENVIRONMENT", None)


def test_production_rejects_default_secret_key():
    """Test that production rejects default SECRET_KEY."""
    os.environ["ENVIRONMENT"] = "production"
    os.environ["SECRET_KEY"] = "your-secret-key-change-in-production"
    
    with pytest.raises(ValueError, match="must be changed from default value"):
        Settings()
    
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("SECRET_KEY", None)


def test_production_requires_minimum_secret_key_length():
    """Test that production requires minimum SECRET_KEY length."""
    os.environ["ENVIRONMENT"] = "production"
    os.environ["SECRET_KEY"] = "short"
    
    with pytest.raises(ValueError, match="at least 32 characters long"):
        Settings()
    
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("SECRET_KEY", None)


def test_production_accepts_valid_secret_key():
    """Test that production accepts valid SECRET_KEY."""
    os.environ["ENVIRONMENT"] = "production"
    os.environ["SECRET_KEY"] = "a" * 32  # Exactly 32 characters
    
    settings = Settings()
    assert settings.secret_key == "a" * 32
    
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("SECRET_KEY", None)


def test_development_allows_missing_secret_key():
    """Test that development allows missing SECRET_KEY."""
    os.environ["ENVIRONMENT"] = "development"
    os.environ.pop("SECRET_KEY", None)
    
    settings = Settings()
    assert settings.secret_key  # Should have a default dev key
    assert "dev-secret-key" in settings.secret_key
    
    os.environ.pop("ENVIRONMENT", None)


def test_testing_allows_missing_secret_key():
    """Test that testing allows missing SECRET_KEY."""
    os.environ["ENVIRONMENT"] = "testing"
    os.environ.pop("SECRET_KEY", None)
    
    settings = Settings()
    assert settings.secret_key  # Should have a default dev key
    
    os.environ.pop("ENVIRONMENT", None)
