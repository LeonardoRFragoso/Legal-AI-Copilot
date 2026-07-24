# Legal AI Copilot — MVP

Sistema de IA para análise de contratos jurídicos com revisão humana, guardrails, e métricas de produtividade.

## Stack

- **Backend**: FastAPI, Python 3.12, SQLAlchemy, Alembic
- **Frontend**: React, TypeScript, Vite, TailwindCSS, Zustand
- **Banco**: SQLite (para MVP sem Docker)
- **IA**: OpenAI GPT-4 (opcional — modo heurístico sem API key)
- **Auth**: JWT (access + refresh tokens), Argon2 password hashing
- **RBAC**: ADMIN, LAWYER, ASSISTANT, CLIENT, VIEWER

## Funcionalidades

- Upload de contratos PDF com extração de texto e chunking
- Agent Router determinístico para classificação de intenção
- Resumo, extração de informações, comparação e análise de riscos
- Análise de riscos heurística (palavras-chave) com severidade e categorias
- Guardrails com validação de confiança e disclaimer jurídico
- Chat com roteamento de agente e persistência de contexto
- Automação pós-upload com webhook (n8n)
- Revisão humana com state machine e histórico append-only
- Métricas de impacto com estimativas de tempo economizado
- Autenticação JWT com RBAC e proteção de rotas no frontend

## Requisitos

- Python 3.12+
- Node.js 18+
- OpenAI API Key (opcional — modo heurístico funciona sem ela)

## Configuração

### Variáveis de Ambiente (Backend)

| Variável | Padrão | Descrição |
|----------|---------|-----------|
| `ENVIRONMENT` | development | Ambiente (development, testing, production) |
| `SECRET_KEY` | (auto-gerado em dev) | Chave JWT — obrigatório em produção |
| `OPENAI_API_KEY` | (vazio) | API key OpenAI — opcional |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Expiração do access token |
| `REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Expiração do refresh token |
| `AUTOMATION_WEBHOOK_ENABLED` | false | Habilita webhook de automação |
| `AUTOMATION_WEBHOOK_URL` | (vazio) | URL do webhook (n8n) |
| `ESTIMATED_MANUAL_SUMMARY_MINUTES` | 30 | Tempo manual estimado para resumo |
| `ESTIMATED_MANUAL_EXTRACTION_MINUTES` | 45 | Tempo manual estimado para extração |
| `ESTIMATED_MANUAL_COMPARISON_MINUTES` | 90 | Tempo manual estimado para comparação |
| `ESTIMATED_MANUAL_QA_MINUTES` | 15 | Tempo manual estimado para Q&A |
| `ESTIMATED_MANUAL_RISK_ANALYSIS_MINUTES` | 120 | Tempo manual estimado para análise de riscos |

### Variáveis de Ambiente (Frontend)

| Variável | Padrão | Descrição |
|----------|---------|-----------|
| `VITE_API_URL` | http://localhost:8000 | URL do backend |
| `VITE_DEMO_MODE` | true | Mostra credenciais demo na tela de login |

## Instalação

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # editar conforme necessário
```

### Migrations

```bash
cd backend
alembic upgrade head
```

### Seed (Usuários Demo)

```bash
cd backend
ENVIRONMENT=development python -m app.seed
```

Cria:
- **LAWYER**: lawyer@demo.com / demo123456
- **ADMIN**: admin@demo.com / admin123456

### Frontend

```bash
cd frontend
npm install
cp .env.example .env  # editar conforme necessário
```

## Execução

```bash
# Terminal 1 — Backend
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Terminal 2 — Frontend
cd frontend
npm run dev
```

Backend: http://localhost:8000
Frontend: http://localhost:5173

## Quick Demo

```bash
# 1. Setup
cd backend && source venv/bin/activate
alembic upgrade head
ENVIRONMENT=development python -m app.seed

# 2. Verificar ambiente
python -m scripts.demo_check

# 3. Resetar dados de demo (opcional)
python -m scripts.demo_reset

# 4. Iniciar backend
uvicorn app.main:app --reload

# 5. Iniciar frontend (outro terminal)
cd frontend && npm run dev
```

Abrir http://localhost:5173, fazer login com credenciais demo, fazer upload de contrato, usar chat e análise.

## Testes

```bash
cd backend
ENVIRONMENT=testing ./venv/bin/python -m pytest -v
```

## Test Status

- **166 tests passed, 0 failed**
- Duração: ~38s
- Cobertura: auth, RBAC, agent router, risk analysis, validators, automation, analysis records, reviews, metrics, smoke test

## Segurança

- Senhas com Argon2
- JWT com expiração
- RBAC em todos os endpoints
- Ownership enforcement (usuários só acessam próprios documentos/análises)
- Credenciais demo só visíveis em modo desenvolvimento (VITE_DEMO_MODE)
- SECRET_KEY obrigatório em produção
- Sem secrets versionados no repositório

## Limitações

- Análise de riscos é heurística (palavras-chave), sem LLM ou RAG semântico
- Citation similarity_score é fixo (0.7), não calculado por embeddings
- Sem OCR (apenas extração de texto PDF)
- Sem refresh token auto-refresh (redirect para login em 401)
- Sem testes frontend automatizados (validado via build TypeScript)
- SQLite (adequado para MVP, PostgreSQL recomendado para produção)
- Métricas são estimativas do MVP, não calibradas com dados reais
- Versioning estrutural apenas (sem regeneração automática)

## Documentação Adicional

- `HUMAN_REVIEW.md` — Workflow de revisão humana
- `IMPACT_METRICS.md` — Métricas de impacto
- `RISK_ANALYSIS.md` — Análise de riscos
- `GUARDRAILS.md` — Guardrails e validação
- `AGENT_EXECUTION.md` — Execução do agente
- `AUTOMATION.md` — Automação e webhook
- `DEMO_SCRIPT.md` — Roteiro de demonstração
- `CASE_PDF_OUTLINE.md` — Estrutura do documento do case
- `CASE_TECHNICAL_NOTES.md` — Notas técnicas e decisões de arquitetura

## Licença

MIT
