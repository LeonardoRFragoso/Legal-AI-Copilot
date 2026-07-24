# Legal AI Copilot — Case Técnico

## PÁGINA 1 — CONTEXTO E SOLUÇÃO

**Projeto**: Legal AI Copilot — MVP de IA para análise de contratos jurídicos

**Problema**: Escritórios de advocacia gastam horas em revisão manual de contratos para identificar cláusulas de risco, extrair informações estruturadas e comparar documentos. O processo é repetitivo, suscetível a erros e consome tempo que poderia ser dedicado a análise estratégica.

**Objetivo do MVP**: Demonstrar um sistema funcional que acelera a análise contratual com IA, mantendo o profissional jurídico no controle por meio de revisão humana obrigatória.

**Público-alvo**: Advogados, assessores jurídicos e administradores de escritórios de advocacia.

**Participação do candidato**: Desenvolvimento full-stack (backend + frontend), arquitetura, integração de IA, guardrails, testes, documentação e preparação de demo.

**Principais funcionalidades**:

- Upload de PDF com extração de texto e chunking
- Chat com agente determinístico (Agent Router) e RAG
- Resumo, extração e comparação via LLM (GPT-4o)
- Análise de riscos heurística (palavras-chave, determinística)
- Guardrails com confidence score, citações e bloqueio de alucinações
- Automação pós-upload com webhook compatível com n8n
- Revisão humana com state machine e histórico append-only
- Métricas de produtividade estimadas
- RBAC com 5 papéis (ADMIN, LAWYER, ASSISTANT, CLIENT, VIEWER)

**Stack**: FastAPI, Python 3.12, SQLAlchemy, Alembic, React, TypeScript, Vite, TailwindCSS, Zustand, SQLite, LangChain, OpenAI GPT-4o, JWT, Argon2.

---

## PÁGINA 2 — ARQUITETURA E IA

### Diagrama de Fluxo

```
Usuário → Frontend (React) → FastAPI → Agent Router (determinístico)
    → Tool (Summary/Extract/Compare/Risk/Q&A)
    → Guardrails (AIValidator) → Persistência (AnalysisRecord)
    → Revisão Humana (AnalysisReview)
```

### Componentes

| Camada | Tecnologia | Descrição |
|--------|-----------|-----------|
| Frontend | React + TypeScript | SPA com auth, chat, análise, revisão, métricas |
| Backend | FastAPI | API REST com JWT, RBAC, BackgroundTasks |
| Banco | SQLite | MVP sem Docker; PostgreSQL recomendado para produção |
| Auth | JWT + Argon2 | Access token (30min) + refresh token (7 dias) |
| IA | OpenAI GPT-4o | Usado em resumo, extração, comparação e Q&A |
| RAG | OpenAI Embeddings | text-embedding-3-small; busca por similaridade cosseno |

### Agent Router

O Agent Router é **determinístico** — classifica a intenção do usuário por palavras-chave, sem chamar LLM. Mapeia para uma de 5 ferramentas: `summarize_document`, `extract_information`, `compare_documents`, `contract_risk_analysis`, `semantic_search`.

### Engenharia de Prompts

Prompts estruturados em português (pt-BR) para GPT-4o:
- **Resumo**: "Faça um resumo detalhado do seguinte documento legal em português"
- **Extração**: Prompt com schema JSON explícito (parties, dates, values, clauses)
- **Comparação**: Prompt comparativo com estrutura de diferenças
- **Q&A**: Via LangChain Agent Executor com histórico de conversa

### Ferramentas e LLM

| Ferramenta | Usa LLM? | Usa RAG? | Usa AIValidator? |
|-----------|----------|----------|-----------------|
| summarize_document | Sim (GPT-4o) | Não | Não |
| extract_information | Sim (GPT-4o) | Não | Não |
| compare_documents | Sim (GPT-4o) | Não | Não |
| contract_risk_analysis | **Não** | **Não** | **Não** |
| semantic_search | Sim (GPT-4o) | Sim (embeddings) | Sim |

---

## PÁGINA 3 — DOCUMENTOS, RAG E CONTROLE DE ALUCINAÇÃO

### Pipeline de Documentos

1. **Upload**: PDF enviado via `POST /documents/upload`
2. **Extração**: Texto extraído com PyPDF2 (sem OCR)
3. **Chunking**: Divisão por sentenças com sobreposição (chunk_size=1000, overlap=200)
4. **Embeddings**: Gerados via OpenAI `text-embedding-3-small`, armazenados como binário (pickle) no SQLite
5. **Busca semântica**: Similaridade cosseno entre embedding da query e embeddings dos chunks

### RAG — Onde é Usado

O RAG (Retrieval-Augmented Generation) é utilizado **apenas na ferramenta `semantic_search`** (Q&A via chat). O fluxo:

```
Pergunta → Embedding da query → Busca cosseno nos chunks → Top-K chunks → Contexto enviado ao GPT-4o → Resposta
```

### Análise de Riscos — Heurística (Separada do RAG)

A análise de riscos é **totalmente determinística**, sem LLM e sem RAG:

- **Camada 1**: HeuristicAnalyzer — detecta cláusulas ausentes (confidencialidade, LGPD, rescisão) e padrões problemáticos (multa ilimitada, renovação automática, pagamento indefinido) por palavras-chave
- **Camada 2**: Recuperação textual — busca chunks relevantes por palavras-chave de risco (não semântica) para gerar citações
- **Camada 3**: Scoring — calcula confidence_score (base 50 + riscos + cobertura) e overall_risk (maior severidade)

**Importante**: O `similarity_score` nas citações da análise de riscos é um valor fixo ilustrativo (0.7), não calculado por embeddings.

### Guardrails (AIValidator)

Aplicado **apenas em Q&A** (`semantic_search`):

- **Confidence score** (0-100): Fontes (30) + Similaridade (30) + Citações (20) + Consistência (10) + Qualidade (10)
- **Bloqueio**: Score < 60 → resposta bloqueada, conteúdo não exposto
- **Citações**: Estruturadas com document_id, chunk_id, page_number, excerpt, similarity_score
- **Disclaimer**: Presente em todas as respostas, mesmo bloqueadas

### Limitações

- Sem OCR (apenas PDF com texto extraível)
- AIValidator não integrado em resumo, extração e comparação
- Análise de riscos não detecta contradições semânticas
- Sem cache de validação

---

## PÁGINA 4 — AUTOMAÇÃO, REVISÃO E SEGURANÇA

### Automação Pós-Upload

Após o upload, `BackgroundTasks` do FastAPI executa:

1. **DOCUMENT_PROCESSING** (10%): Verifica documento
2. **SUMMARY** (30-50%): Executa `summarize_document` (GPT-4o)
3. **RISK_ANALYSIS** (70-85%): Executa `RiskAnalyzer.analyze()` (heurístico)
4. **WEBHOOK** (90%): Envia evento `analysis.completed`
5. **COMPLETED** (100%): Finaliza AutomationRun

Cada execução é persistida como `AutomationRun` com status, progresso, resultados e webhook_status.

### Webhook e n8n

- Webhook HTTP POST com payload estruturado (event, document, analysis)
- Features: idempotency key, retry configurável, timeout
- Workflow n8n de exemplo disponível em `n8n/analysis-completed-workflow.json`
- **Não necessariamente executado em ambiente externo** — é um workflow de exemplo importável

### Revisão Humana

- **AnalysisRecord**: Persiste toda análise gerada (chat, endpoint direto, automação)
- **State Machine**: GENERATED → PENDING_REVIEW → APPROVED/REJECTED/NEEDS_CHANGES
- **AnalysisReview**: Histórico append-only (nunca modificado ou deletado)
- **RBAC**: ADMIN revisa tudo; LAWYER revisa próprias; ASSISTANT apenas visualiza
- **Bloqueio**: Análises bloqueadas não podem ser aprovadas

### Segurança

| Aspecto | Implementação |
|---------|--------------|
| Autenticação | JWT (HS256), access + refresh tokens |
| Senhas | Argon2 via passlib |
| RBAC | 5 papéis com verificação por endpoint |
| Ownership | Usuários acessam apenas próprios documentos/análises |
| Demo mode | Credenciais demo só visíveis com `VITE_DEMO_MODE=true` |
| SECRET_KEY | Obrigatório em produção |
| Sem secrets versionados | `.env` em `.gitignore` |

### Limitação do BackgroundTasks

FastAPI `BackgroundTasks` executa no processo da aplicação. Não há fila externa (Celery/RQ). Em produção com múltipres workers, tarefas podem ser perdidas em restart. Recomenda-se Celery + Redis para produção.

---

## PÁGINA 5 — RESULTADOS, TESTES E PRÓXIMOS PASSOS

### Testes

```
166 passed, 0 failed
```

| Arquivo | Cobertura |
|---------|-----------|
| test_auth.py | JWT, RBAC, login, refresh, logout |
| test_api.py | Endpoints, auth enforcement |
| test_validators.py | Extração, resumo, chat, confiança |
| test_agent_router.py | Classificação de intenção |
| test_agent_chat_integration.py | Chat end-to-end com LLM mockado |
| test_risk_analysis.py | Análise heurística de riscos |
| test_automation.py | Pipeline, webhook, retry |
| test_analysis_review.py | Records, reviews, state machine, métricas |
| test_demo_smoke.py | Fluxo completo de demo, guardrails, RBAC |

### Validações

- **Migrations**: upgrade/downgrade/re-upgrade validados
- **Frontend**: `tsc && vite build` — PASS
- **Smoke tests**: Fluxo completo (auth → upload → análise → revisão → métricas)
- **Git**: `git diff --check` — sem erros de whitespace

### Métricas Estimadas

**Os ganhos de produtividade apresentados são estimativas do MVP e não resultados medidos em produção.**

Tempos manuais configuráveis: Resumo (30min), Extração (45min), Comparação (90min), Q&A (15min), Análise de Riscos (120min).

### Limitações Conhecidas

1. Análise de riscos é heurística (sem LLM/RAG semântico)
2. `similarity_score` nas citações de risco é fixo (0.7)
3. Sem OCR
4. Sem refresh token auto-refresh
5. Sem testes frontend automatizados
6. SQLite (PostgreSQL recomendado para produção)
7. AIValidator apenas em Q&A (não em resumo/extração/comparação)
8. BackgroundTasks sem fila externa

### Próximos Passos

- Integrar AIValidator em todas as operações com LLM
- Adicionar RAG semântico à análise de riscos
- Migrar para PostgreSQL + Celery
- Implementar OCR
- Calibrar métricas com dados reais
- Adicionar testes frontend (Vitest/Playwright)

### GitHub

https://github.com/LeonardoRFragoso/Legal-AI-Copilot
