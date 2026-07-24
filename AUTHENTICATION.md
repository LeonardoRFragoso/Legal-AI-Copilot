# Autenticação e RBAC - Legal AI Copilot

## Visão Geral

O Legal AI Copilot implementa um sistema seguro de autenticação baseado em JWT (JSON Web Tokens) com controle de acesso baseado em papéis (RBAC - Role-Based Access Control).

## Fluxo JWT

### 1. Registro (Register)

```
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePassword123",
  "role": "lawyer"  // opcional, padrão: "viewer"
}

Response (201):
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "lawyer",
  "is_active": true,
  "created_at": "2026-07-24T...",
  "last_login": null
}
```

### 2. Login

```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePassword123"
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800  // segundos (30 minutos)
}
```

### 3. Usando o Access Token

Todos os endpoints protegidos requerem o header:

```
Authorization: Bearer <access_token>
```

Exemplo:
```
GET /documents
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### 4. Refresh Token

Quando o access token expira, use o refresh token para obter um novo:

```
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}

Response (200):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 5. Logout

```
POST /auth/logout
Authorization: Bearer <access_token>

Response (200):
{
  "message": "Logged out successfully"
}
```

### 6. Obter Usuário Atual

```
GET /auth/me
Authorization: Bearer <access_token>

Response (200):
{
  "id": "uuid",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "lawyer",
  "is_active": true,
  "created_at": "2026-07-24T...",
  "last_login": "2026-07-24T..."
}
```

## Papéis (Roles)

### ADMIN
- Acesso total a todos os recursos
- Pode gerenciar usuários
- Pode acessar documentos de qualquer usuário
- Pode acessar conversas de qualquer usuário

### LAWYER
- Pode fazer upload de documentos
- Pode analisar documentos (summary, extract, compare)
- Pode criar e participar de conversas
- Pode acessar apenas seus próprios documentos e conversas

### ASSISTANT
- Pode fazer upload de documentos
- Pode analisar documentos
- Pode criar e participar de conversas
- Pode acessar apenas seus próprios documentos e conversas

### CLIENT
- Pode criar e participar de conversas
- Pode acessar apenas seus próprios documentos e conversas
- Não pode fazer upload de documentos

### VIEWER
- Acesso somente leitura
- Pode visualizar documentos compartilhados
- Não pode fazer upload
- Não pode criar conversas

## RBAC - Controle de Acesso

### Endpoints Públicos (sem autenticação)
- `GET /` - Root
- `GET /health` - Health check

### Endpoints Protegidos

#### Documentos
- `POST /documents/upload` - Requer: LAWYER, ASSISTANT, ADMIN
- `GET /documents` - Requer: Autenticado (vê apenas seus documentos)
- `GET /documents/{id}` - Requer: Autenticado (acesso ao seu documento)
- `DELETE /documents/{id}` - Requer: LAWYER, ASSISTANT, ADMIN (seu documento)

#### Análises
- `POST /analysis/summary` - Requer: Autenticado (seu documento)
- `POST /analysis/extract` - Requer: Autenticado (seu documento)
- `POST /analysis/compare` - Requer: Autenticado (seus documentos)

#### Conversas
- `POST /conversations` - Requer: Autenticado
- `GET /conversations` - Requer: Autenticado (suas conversas)
- `POST /conversations/{id}/messages` - Requer: Autenticado (sua conversa)
- `GET /conversations/{id}/messages` - Requer: Autenticado (sua conversa)

## Segurança

### Hash de Senha
- Utiliza bcrypt com salt automático
- Senhas nunca são armazenadas em texto plano
- Mínimo 8 caracteres

### JWT
- Algoritmo: HS256
- Access Token: Expira em 30 minutos
- Refresh Token: Expira em 7 dias
- Secret Key: Configurável via variável de ambiente `SECRET_KEY`

### Isolamento de Dados
- Usuários veem apenas seus próprios documentos e conversas
- ADMINs podem acessar tudo
- Verificação de acesso em cada endpoint

## Variáveis de Ambiente

```bash
# .env
SECRET_KEY=your-super-secret-key-change-in-production
OPENAI_API_KEY=sk-...
```

## Exemplo de Fluxo Completo

```bash
# 1. Registrar
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Lawyer",
    "email": "john@law.com",
    "password": "SecurePassword123",
    "role": "lawyer"
  }'

# 2. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@law.com",
    "password": "SecurePassword123"
  }'

# Resposta contém access_token

# 3. Usar o token
curl -X GET http://localhost:8000/documents \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

# 4. Refresh token quando expirar
curl -X POST http://localhost:8000/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
  }'

# 5. Logout
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

## Testes

Execute os testes de autenticação:

```bash
cd backend
pytest tests/test_auth.py -v
```

Cobertura de testes:
- ✓ Criação de token JWT
- ✓ Expiração de token
- ✓ Registro de usuário
- ✓ Login bem-sucedido
- ✓ Login com credenciais inválidas
- ✓ Refresh token
- ✓ Logout
- ✓ Obter usuário atual
- ✓ Proteção de endpoints
- ✓ RBAC (acesso baseado em papel)

## Tratamento de Erros

### 400 Bad Request
- Email já registrado
- Dados inválidos

### 401 Unauthorized
- Token ausente ou inválido
- Credenciais incorretas
- Token expirado

### 403 Forbidden
- Usuário não tem permissão para acessar o recurso
- Papel insuficiente

### 404 Not Found
- Recurso não encontrado

## Boas Práticas

1. **Sempre use HTTPS em produção**
2. **Mantenha SECRET_KEY segura**
3. **Não exponha tokens em URLs**
4. **Implemente refresh token rotation**
5. **Monitore tentativas de login falhadas**
6. **Implemente rate limiting em endpoints de autenticação**
7. **Use tokens com expiração curta**
