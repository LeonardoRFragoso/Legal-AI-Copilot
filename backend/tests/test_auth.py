import pytest
from datetime import timedelta
from app.auth import create_access_token, verify_token, SECRET_KEY, ALGORITHM
import jwt


def test_create_access_token():
    """Testa criação de token JWT"""
    data = {"sub": "user123"}
    token = create_access_token(data)
    
    assert token is not None
    assert isinstance(token, str)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user123"


def test_create_access_token_with_expiration():
    """Testa criação de token com expiração customizada"""
    data = {"sub": "user123"}
    expires_delta = timedelta(minutes=5)
    token = create_access_token(data, expires_delta)
    
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user123"
    assert "exp" in payload


def test_token_expiration():
    """Testa expiração de token"""
    data = {"sub": "user123"}
    expires_delta = timedelta(seconds=-1)
    token = create_access_token(data, expires_delta)
    
    with pytest.raises(jwt.ExpiredSignatureError):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def test_invalid_token():
    """Testa token inválido"""
    invalid_token = "invalid.token.here"
    
    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(invalid_token, SECRET_KEY, algorithms=[ALGORITHM])
