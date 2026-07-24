# PHASE 2 - ETAPA 3 PRECHECK

**Data:** 24 de Julho de 2026

---

## Auditoria do Código Real

### Agent Router (`app/agent_router.py`)

- **Status:** ✅ Existe e funcional
- **Intents:** 6 (SUMMARIZE, EXTRACT, COMPARE, QUESTION_ANSWERING, IDENTIFY_RISKS, UNKNOWN)
- **Classificação:** Determinística por keywords (PT/EN)
- **Integração com chat:** ❌ NÃO integrado — o chat usa `legal_agent.query()` diretamente, sem passar pelo router
- **`RouterDecision`:** Dataclass com intent, tool, reason, required_documents, confidence
- **`to_dict()` bug:** Método na classe em vez de na instância (não é chamado corretamente)

### Chat (`app/main.py` linhas 301-401)

- **Endpoint:** `POST /conversations/{conversation_id}/messages`
- **Fluxo atual:** mensagem → `legal_agent.query()` → `AIValidator.validate()` → persistir
- **Problema:** Não usa Agent Router; sempre chama o agente LangChain
- **Document_id:** Vem de `conversation.document_id`
- **Mensagens:** Persistidas via `ConversationRepository.add_message()` com citations em JSON
- **Acesso:** RBAC verificado (ADMIN ou owner)

### Upload (`app/main.py` linhas 66-126)

- **Endpoint:** `POST /documents/upload`
- **Fluxo:** upload → extrair PDF → chunking → embeddings → update status "ready"
- **Síncrono:** Todo o processamento é síncrono
- **BackgroundTasks:** ❌ Não utilizado
- **Pós-upload:** ❌ Sem automação (sem resumo automático, sem análise de riscos)
- **Status do documento:** "processing" → "ready"

### Modelos (`app/models.py`)

- **User, Document, Chunk, DocumentEmbedding, Conversation, Message**
- **❌ Sem AutomationRun** — precisa ser criado
- **Banco:** SQLite (`sqlite:///./legal_ai.db`)
- **create_all:** Usado para criar tabelas (sem migrations versionadas)

### Infraestrutura Assíncrona

- **BackgroundTasks do FastAPI:** ✅ Disponível (não usado atualmente)
- **Celery/RQ/Dramatiq:** ❌ Não configurado
- **Redis:** ❌ Não configurado
- **Fila durável:** ❌ Não existe

### Migrations

- **Alembic:** ❌ Não configurado no projeto (apenas no venv)
- **create_all:** Único método usado para criar tabelas
- **Decisão:** Configurar Alembic + criar migration para `automation_runs`

### Guardrails (`app/ai_validator.py`)

- **Status:** ✅ Funcional
- **AIValidator:** Score determinístico, blocking, citations, disclaimer
- **Integração:** Já usado no chat, precisa ser reutilizado na automação

### Risk Analysis (`app/risk_analysis.py`)

- **Status:** ✅ Funcional
- **RiskAnalyzer:** Heurísticas + RAG retrieval + scoring
- **Endpoint:** `POST /analysis/risks`
- **Integração com chat:** ❌ Não integrado

### Frontend

- **Chat (`Chat.tsx`):** Renderiza mensagens como texto plano, citations como texto
- **Risk Analysis (`RiskAnalysis.tsx`):** Página dedicada com severity badges
- **❌ Sem página de automações**
- **❌ Sem renderização estruturada de riscos no chat**

### Configuração (`app/config.py`)

- **Settings:** Pydantic BaseSettings com thresholds de validação
- **❌ Sem configurações de webhook**

---

## Riscos Técnicos

1. **SQLite + BackgroundTasks:** Tarefas em background podem ter problemas de concorrência com SQLite (check_same_thread=False já configurado)
2. **Sem fila durável:** Tarefas podem ser perdidas se o processo reiniciar
3. **Sem Alembic:** Precisa configurar do zero
4. **Chat síncrono:** Atualmente bloqueia até o agente responder

---

## Decisões de Implementação

1. **Agent Router no chat:** Substituir `legal_agent.query()` por router → executar tool apropriada
2. **Serviços reutilizáveis:** Extrair lógica de resumo, extração, comparação, riscos para funções chamáveis
3. **BackgroundTasks:** Usar para automação pós-upload (com documentação de limitações)
4. **Alembic:** Configurar do zero com migration para `automation_runs`
5. **Webhook:** Usar `httpx` (já disponível no venv?) ou `requests` para enviar POST
6. **Frontend chat:** Renderizar respostas estruturadas de riscos de forma legível
7. **Frontend automação:** Criar página `/automations` simples
