import pytest
from datetime import timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.auth import create_access_token, verify_token, SECRET_KEY, ALGORITHM, hash_password
from app.models import User, UserRole
import jwt

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Limpa o banco de dados antes de cada teste"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


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


# Integration tests
def test_register_user():
    """Testa registro de novo usuário"""
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["role"] == "viewer"
    assert data["is_active"] is True


def test_register_duplicate_email():
    """Testa registro com email duplicado"""
    # Primeiro registro
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    # Segundo registro com mesmo email
    response = client.post(
        "/auth/register",
        json={
            "name": "Another User",
            "email": "test@example.com",
            "password": "TestPass456"
        }
    )
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success():
    """Testa login bem-sucedido"""
    # Registrar usuário
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    # Login
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_password():
    """Testa login com senha incorreta"""
    # Registrar usuário
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    # Login com senha errada
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass789"
        }
    )
    
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_login_nonexistent_user():
    """Testa login com usuário inexistente"""
    response = client.post(
        "/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "TestPass000"
        }
    )
    
    assert response.status_code == 401


def test_refresh_token():
    """Testa refresh de token"""
    # Registrar e fazer login
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    refresh_token = login_response.json()["refresh_token"]
    
    # Usar refresh token
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_logout():
    """Testa logout"""
    # Registrar e fazer login
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    access_token = login_response.json()["access_token"]
    
    # Logout
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200


def test_get_current_user():
    """Testa obtenção do usuário atual"""
    # Registrar e fazer login
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "TestPass123"
        }
    )
    
    access_token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"


def test_protected_endpoint_without_token():
    """Testa acesso a endpoint protegido sem token"""
    response = client.get("/documents")
    
    assert response.status_code == 401


def test_protected_endpoint_with_invalid_token():
    """Testa acesso a endpoint protegido com token inválido"""
    response = client.get(
        "/documents",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    
    assert response.status_code == 401


def test_rbac_lawyer_access():
    """Testa acesso de usuário LAWYER"""
    # Registrar como LAWYER
    register_response = client.post(
        "/auth/register",
        json={
            "name": "Lawyer User",
            "email": "lawyer@example.com",
            "password": "TestPass123",
            "role": "lawyer"
        }
    )
    
    assert register_response.status_code == 201
    assert register_response.json()["role"] == "lawyer"
    
    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "email": "lawyer@example.com",
            "password": "TestPass123"
        }
    )
    
    access_token = login_response.json()["access_token"]
    
    # Acessar endpoint protegido
    response = client.get(
        "/documents",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert response.status_code == 200


def test_rbac_viewer_cannot_upload():
    """Testa que VIEWER não pode fazer upload"""
    # Registrar como VIEWER (default)
    client.post(
        "/auth/register",
        json={
            "name": "Viewer User",
            "email": "viewer@example.com",
            "password": "TestPass123"
        }
    )
    
    login_response = client.post(
        "/auth/login",
        json={
            "email": "viewer@example.com",
            "password": "TestPass123"
        }
    )
    
    access_token = login_response.json()["access_token"]
    
    # Tentar fazer upload
    response = client.post(
        "/documents/upload",
        headers={"Authorization": f"Bearer {access_token}"},
        data={"title": "Test Document"},
        files={"file": ("test.pdf", b"fake pdf content")}
    )
    
    assert response.status_code == 403
