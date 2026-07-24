# PHASE 2 — STAGE 4 PRECHECK

## Estado Real do Repositório (commit 12152d3)

### Backend

**Modelos existentes (`app/models.py`):**
- `User` (id, name, email, password_hash, role, is_active, timestamps)
- `Document` (id, user_id, title, filename, file_path, status, page_count, created_at)
- `Chunk` (id, document_id, chunk_index, text, page_number, chunk_metadata)
- `DocumentEmbedding` (id, chunk_id, document_id, embedding binary)
- `Conversation` (id, user_id, document_id, title, created_at)
- `Message` (id, conversation_id, role, content, citations JSON, created_at)
- `AutomationRun` (id, document_id, user_id, automation_type, status, current_step, progress_percent, started_at, completed_at, error_message, summary_result JSON, risk_result JSON, webhook_status, webhook_error, timestamps)

**NÃO existe:**
- `AnalysisRecord` — nenhum modelo de análise persistida e identificável
- `AnalysisReview` — nenhum modelo de revisão humana
- Nenhum histórico de revisão
- Nenhum endpoint de métricas de impacto

**Onde resultados são persistidos hoje:**
- Resumo: `AutomationRun.summary_result` (JSON `{"summary": "..."}`)
- Risco: `AutomationRun.risk_result` (JSON com `to_dict()` do `RiskAnalysisResult`)
- Chat: `Message.citations` (JSON com agent metadata, structured_data, validation, disclaimer)
- **Não há entidade reutilizável para análises** — tudo é JSON em AutomationRun ou Message

**Endpoint `/admin/system-status`:**
- Usa dados reais do banco (conta AutomationRun, Document, webhooks falhos)
- Não retorna análises bloqueadas ou pendentes de revisão (não existem)
- ADMIN only — correto

**Autenticação:**
- Backend completo: `/auth/login`, `/auth/register`, `/auth/refresh`, `/auth/me`, `/auth/logout`
- JWT com access + refresh tokens
- RBAC com `require_role()` — funciona corretamente
- **Nenhum seed script** — não há usuário LAWYER de demonstração

### Frontend

**Páginas existentes:**
- Dashboard (lista documentos)
- Upload (form simples)
- Chat (com Agent Router integration)
- Analysis (resumo + extração)
- RiskAnalysis (análise de riscos)
- Comparison (comparar documentos)
- Automations (lista de runs com progresso)

**NÃO existe:**
- **Página de Login** — nenhuma rota `/login`
- **Página de Registro** — nenhuma rota
- **Auth store** — zustand store não gerencia auth
- **Interceptador Authorization** — `api.ts` não envia token
- **Página de Revisão/Análises** — não existe
- **Página de Métricas/Insights** — não existe
- **Proteção de rotas** — nenhuma guarda de rota

**Risco crítico para demo:**
- O frontend **não consegue autenticar** — todas as chamadas API falham com 401
- Após recarregar o navegador, **não há sessão persistida**
- Não há como um usuário LAWYER acessar a aplicação

### Testes

- **136 testes coletados** (não 117 como relatado anteriormente)
- Arquivos: test_auth.py, test_config.py, test_ai_validator.py, test_agent_router.py, test_risk_analysis.py, test_agent_chat_integration.py, test_automation.py, test_api.py, test_validators.py
- conftest.py compartilha DB de teste

### Migrations

- 1 migration: `4f38586d77d6` (automation_runs table)
- Alembic configurado corretamente com `app.database.Base`

### .gitignore

- Cobre: .env, *.db, *.log, uploads/, __pycache__/, node_modules/, dist/
- Adequado para o escopo

---

## Inconsistências Encontradas

1. **Frontend sem autenticação** — backend tem auth completo, frontend não usa
2. **Sem persistência de análises identificáveis** — resultados apenas em JSON ad-hoc
3. **Número de testes incorreto nos relatórios** — 136, não 117
4. **Sem seed de demonstração** — não há usuário LAWYER para a demo
5. **Dashboard não mostra métricas** — apenas lista documentos
6. **n8n workflow apenas criado, não validado estruturalmente** — JSON existe mas não testado

---

## Riscos para a Demonstração

1. **ALTO: Demo quebra sem login** — frontend não envia token, todas as APIs retornam 401
2. **ALTO: Sessão perdida ao recarregar** — sem persistência de token
3. **MÉDIO: Sem usuário LAWYER** — não há seed, registro público cria CLIENT
4. **MÉDIO: Sem revisão humana** — não é possível demonstrar workflow de aprovação
5. **BAIXO: Sem métricas** — dashboard não mostra impacto

---

## Decisões Arquiteturais

1. **AnalysisRecord como novo modelo** — não reusar AutomationRun (sem structured_result, sem status de revisão)
2. **AnalysisReview append-only** — histórico imutável de decisões
3. **analysis_record_service.py** — serviço reutilizável para criar/atualizar registros
4. **Auth store com zustand + localStorage** — persistir token entre recargas
5. **Login page mínima** — email + senha, sem registro público
6. **Seed script** — criar usuário LAWYER de demonstração via script Python
7. **Regenerate endpoint** — adiar se adicionar complexidade excessiva

---

## Itens que Serão Corrigidos

1. Login frontend + auth store + interceptador axios
2. Sessão persistida via localStorage
3. Seed script para usuário LAWYER
4. AnalysisRecord + AnalysisReview models
5. analysis_record_service.py
6. Endpoints de análise e revisão
7. Migration Alembic para novas tabelas
8. Página de revisão no frontend
9. Métricas de impacto + dashboard
10. Melhoria do system-status
11. Testes backend

---

## Itens Conscientemente Adiados

1. **Regenerate endpoint** — avaliar viabilidade; se instável, documentar apenas versionamento
2. **Testes frontend automatizados** — sem framework configurado; validar com build
3. **Validação estrutural do n8n workflow** — JSON existe, validação manual documentada
4. **Refresh token automático no frontend** — apenas se suporte estável existir
5. **Registro público no frontend** — fora do escopo da demo
