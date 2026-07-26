# Detalhes Técnicos Complementares — Legal AI Copilot

Este documento complementa o roteiro principal com informações técnicas profundas.

---

## 1. RAG — Detalhamento Completo

### Fluxo de Recuperação

```
1. Pergunta do usuário: "Qual é o valor do contrato?"
   ↓
2. Gerar embedding da pergunta
   - Usar modelo text-embedding-3-small
   - Resultado: vetor de 1536 dimensões
   ↓
3. Recuperar embeddings dos chunks do banco
   - Query: SELECT embedding FROM document_embeddings WHERE document_id = ?
   ↓
4. Calcular similaridade de cosseno
   - Para cada chunk: similarity = (pergunta · chunk) / (||pergunta|| × ||chunk||)
   ↓
5. Ordenar por similaridade (descendente)
   ↓
6. Selecionar top-5 chunks
   ↓
7. Construir contexto
   - Concatenar os 5 chunks
   - Adicionar informações de página
   ↓
8. Enviar ao modelo
   - Prompt: "Responda baseado neste contexto: [chunks]"
   - Pergunta: "Qual é o valor do contrato?"
   ↓
9. Modelo gera resposta
   ↓
10. Validar resposta
    - Calcular score de confiança
    - Extrair citações
    - Bloquear se necessário
```

### Cálculo de Similaridade de Cosseno

**Fórmula**:
```
similarity(a, b) = (a · b) / (||a|| × ||b||)

Onde:
- a · b = produto escalar (sum of a[i] * b[i])
- ||a|| = norma euclidiana (sqrt(sum of a[i]²))
- ||b|| = norma euclidiana (sqrt(sum of b[i]²))
```

**Interpretação**:
- 1.0 = vetores idênticos
- 0.5 = moderadamente similares
- 0.0 = completamente diferentes
- -1.0 = opostos (raro em embeddings de texto)

**Exemplo com números pequenos**:
```
Pergunta: [0.1, 0.2, 0.3]
Chunk 1:  [0.1, 0.2, 0.32]  → similarity ≈ 0.998 (muito similar)
Chunk 2:  [0.05, 0.1, 0.15] → similarity ≈ 0.995 (muito similar)
Chunk 3:  [0.9, 0.8, 0.7]   → similarity ≈ 0.42 (pouco similar)
```

### Threshold de Similaridade

**Configurado em**: `backend/app/config.py`

```python
MIN_SIMILARITY_SCORE = 0.3  # Mínimo para considerar chunk relevante
```

**Interpretação**:
- Chunks com similaridade < 0.3 são descartados
- Chunks com similaridade ≥ 0.3 são considerados relevantes
- Top-5 são recuperados (mesmo que alguns tenham similaridade baixa)

**Ajuste recomendado**:
- Aumentar para 0.5 se muitos chunks irrelevantes forem recuperados
- Diminuir para 0.2 se chunks relevantes forem perdidos

### Armazenamento de Embeddings

**Tabela**: `document_embeddings`

```sql
CREATE TABLE document_embeddings (
    id VARCHAR(36) PRIMARY KEY,
    chunk_id VARCHAR(36) NOT NULL,
    document_id VARCHAR(36) NOT NULL,
    embedding BLOB NOT NULL,  -- Vetor serializado com pickle
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chunk_id) REFERENCES chunks(id),
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

**Serialização**:
```python
import pickle

# Salvar
embedding_vector = [0.1, 0.2, 0.3, ...]  # 1536 dimensões
embedding_blob = pickle.dumps(embedding_vector)
db.add(DocumentEmbedding(embedding=embedding_blob))

# Recuperar
embedding_blob = db.query(DocumentEmbedding).first().embedding
embedding_vector = pickle.loads(embedding_blob)
```

**Tamanho em disco**:
- Cada embedding: ~6.1 KB (1536 floats × 4 bytes)
- 1000 chunks: ~6.1 MB
- 10000 chunks: ~61 MB

---

## 2. Chunking — Estratégia Detalhada

### Parâmetros

```python
chunk_size = 1000      # Caracteres por chunk
overlap = 200          # Caracteres de sobreposição (20%)
step = chunk_size - overlap = 800  # Deslocamento entre chunks
```

### Exemplo Visual

```
Texto original: "CLÁUSULA 1: Valor. O contrato tem valor de R$ 50.000. 
                 CLÁUSULA 2: Pagamento. Pagamento em 12 parcelas. 
                 CLÁUSULA 3: Rescisão. Rescisão por acordo mútuo."

Chunk 1 (chars 0-1000):
"CLÁUSULA 1: Valor. O contrato tem valor de R$ 50.000. 
 CLÁUSULA 2: Pagamento. Pagamento em 12 parcelas. 
 CLÁUSULA 3: Rescisão..."

Chunk 2 (chars 800-1800, com 200 chars de overlap):
"...Pagamento em 12 parcelas. 
 CLÁUSULA 3: Rescisão. Rescisão por acordo mútuo. 
 CLÁUSULA 4: ..."
```

### Motivo da Sobreposição

Sem sobreposição:
```
Chunk 1: "...Pagamento em 12 parcelas."
Chunk 2: "CLÁUSULA 3: Rescisão..."
         ↑ Informação perdida na transição
```

Com sobreposição:
```
Chunk 1: "...Pagamento em 12 parcelas. CLÁUSULA 3: Rescisão..."
Chunk 2: "...CLÁUSULA 3: Rescisão. Rescisão por acordo mútuo..."
         ↑ Informação preservada em ambos os chunks
```

### Estimativa de Página

```python
def _estimate_page(self, char_position: int, text: str) -> int:
    """Estimar número da página baseado na posição do caractere."""
    # Assumir ~3000 caracteres por página
    return (char_position // 3000) + 1
```

**Limitação**: Esta é uma estimativa. Para precisão, seria necessário rastrear quebras de página durante a extração do PDF.

---

## 3. Embeddings — Modelo e Custo

### Modelo Utilizado

**Nome**: `text-embedding-3-small` (OpenAI)

**Características**:
- **Dimensionalidade**: 1536
- **Tempo de resposta**: ~100ms por chunk
- **Custo**: $0.00001 por 1000 tokens (aproximadamente $0.00001 por chunk)
- **Limite de tokens**: 8191 por requisição

### Custo Estimado

```
Contrato de 10 páginas:
- Aproximadamente 30000 caracteres
- Dividido em ~30 chunks
- Custo: 30 × $0.00001 = $0.0003 por contrato

1000 contratos por mês:
- Custo total: 1000 × $0.0003 = $0.30 por mês
```

### Alternativas de Embeddings

| Modelo | Dimensionalidade | Custo | Vantagem |
|--------|------------------|-------|----------|
| text-embedding-3-small | 1536 | $0.00001 | Custo baixo, qualidade boa |
| text-embedding-3-large | 3072 | $0.00013 | Qualidade superior |
| text-embedding-ada-002 | 1536 | $0.0001 | Modelo anterior (mais barato) |
| Llama 2 (local) | 4096 | Grátis | Sem custo, sem latência de API |

---

## 4. Score de Confiança — Fórmula Detalhada

### Componentes

#### 1. Fontes (até 30 pontos)

```python
if len(chunks) == 0:
    points = 0
elif len(chunks) == 1:
    points = 10
elif len(chunks) <= 3:
    points = 20
else:  # 4+
    points = 30
```

**Lógica**: Mais chunks = mais evidência

#### 2. Similaridade (até 30 pontos)

```python
avg_similarity = sum(similarities) / len(similarities)

if avg_similarity >= 0.80:
    points = 30
elif avg_similarity >= 0.60:
    points = 20
elif avg_similarity >= 0.30:
    points = 10
else:
    points = 0
```

**Lógica**: Chunks mais similares = mais confiança

#### 3. Citações (até 20 pontos)

```python
if len(citations) >= 3:
    points = 20
elif len(citations) >= 1:
    points = 10
else:
    points = 0
```

**Lógica**: Mais citações = melhor rastreabilidade

#### 4. Consistência (até 10 pontos)

```python
if sources_score >= 20 and citations_score >= 10:
    points = 10
else:
    points = 0
```

**Lógica**: Boas fontes + boas citações = resposta consistente

#### 5. Qualidade (até 10 pontos)

```python
significant_chunks = sum(1 for chunk in chunks if len(chunk.text) > 50)
percentage = significant_chunks / len(chunks)

if percentage >= 0.80:
    points = 10
elif percentage >= 0.50:
    points = 5
else:
    points = 0
```

**Lógica**: Chunks com conteúdo significativo = qualidade

### Fórmula Final

```
confidence_score = sources + similarity + citations + consistency + quality
```

**Intervalo**: 0-100

**Classificação**:
- 80-100: HIGH (alta sustentação documental)
- 60-79: MODERATE (evidência adequada com lacunas)
- 0-59: LOW (evidência insuficiente) → **BLOQUEADO**

---

## 5. Análise de Riscos — Palavras-Chave

### Categorias de Risco

#### 1. Confidencialidade

```python
CONFIDENTIALITY_KEYWORDS = {
    "confidencial", "confidentiality", "sigilo", "secret",
    "proprietary", "proprietário", "nda", "non-disclosure"
}
```

**Risco**: Se nenhuma palavra-chave encontrada, risco MÉDIO de falta de cláusula

#### 2. LGPD (Lei Geral de Proteção de Dados)

```python
LGPD_KEYWORDS = {
    "lgpd", "proteção de dados", "dados pessoais", "gdpr",
    "consentimento", "titular", "processamento"
}
```

**Risco**: Se nenhuma palavra-chave encontrada, risco ALTO de não-conformidade

#### 3. Rescisão

```python
TERMINATION_KEYWORDS = {
    "rescisão", "termination", "rescisão", "término",
    "encerramento", "cancelamento"
}
```

**Risco**: Se nenhuma palavra-chave encontrada, risco MÉDIO

#### 4. Multa Ilimitada

```python
UNLIMITED_PENALTY_KEYWORDS = {
    "multa ilimitada", "unlimited penalty", "sem teto",
    "sem limite", "indefinida"
}
```

**Risco**: Se encontrada, risco CRÍTICO

#### 5. Renovação Automática

```python
AUTO_RENEWAL_KEYWORDS = {
    "renovação automática", "auto-renewal", "automatically renewed",
    "renovado automaticamente"
}
```

**Risco**: Se encontrada, risco MÉDIO

#### 6. Pagamento Indefinido

```python
INDEFINITE_PAYMENT_KEYWORDS = {
    "pagamento indefinido", "indefinitely", "indefinidamente",
    "sem prazo", "perpetual"
}
```

**Risco**: Se encontrada, risco ALTO

### Severidade dos Riscos

| Severidade | Pontos | Significado |
|-----------|--------|-------------|
| LOW | 1-25 | Risco menor, não requer ação imediata |
| MEDIUM | 26-50 | Risco moderado, requer revisão |
| HIGH | 51-75 | Risco significativo, requer ação |
| CRITICAL | 76-100 | Risco grave, requer ação imediata |

---

## 6. Prompts — Análise Detalhada

### Prompt do Sistema (Legal Agent)

**Localização**: `backend/app/legal_agent.py:260-275`

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", """Você é um assistente de Legal AI Copilot especializado em análise de contratos. 
    Seu papel é ajudar os usuários a entender documentos legais pesquisando informações, 
    resumindo documentos, extraindo informações-chave e comparando documentos.
    
    REGRAS IMPORTANTES:
    - Sempre baseie suas respostas no conteúdo do documento recuperado pela ferramenta de busca
    - Se a informação não for encontrada nos documentos, diga "Não encontrei essa informação no documento enviado."
    - Nunca invente ou alucine informações
    - Sempre cite o documento de origem e o número da página ao fornecer informações
    - Seja preciso e profissional em suas respostas
    - SEMPRE responda em português (pt-BR)"""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])
```

**Análise**:
1. **Definição de Papel**: "Você é um assistente especializado em análise de contratos"
2. **Contexto**: Explica as ferramentas disponíveis
3. **Regras**: 6 regras explícitas para reduzir alucinações
4. **Idioma**: Força resposta em português

### Prompt de Extração

**Localização**: `backend/app/legal_agent.py:153-184`

```python
prompt = f"""Extract the following information from this legal document and return ONLY a valid JSON object with no additional text:

{{
  "parties": [
    {{"name": "party name", "role": "contratante/contratada/ambos", "description": "brief description"}}
  ],
  "dates": [
    {{"date": "DD/MM/YYYY or description", "type": "inicio/termino/renovacao/prazo", "description": "what this date means"}}
  ],
  "values": [
    {{"amount": "value with currency", "type": "salario_mensal/salario_total/multa/taxa/outro", "description": "detailed explanation of what this value is for"}}
  ],
  "clauses": [
    {{"clause": "clause name", "type": "confidencialidade/multa/rescisao/pagamento/lgpd/outro", "description": "detailed explanation", "risk": "baixo/medio/alto"}}
  ]
}}

IMPORTANT RULES:
1. For parties: Identify WHO is contracting WHO. Be specific about roles.
2. For dates: Explain WHAT each date means (e.g., "Contract starts on 01/08/2026" not just "01/08/2026")
3. For values: Distinguish between salario_mensal, salario_total, multa, taxa
4. For clauses: Provide DETAILED explanations of what each clause means and its implications.
5. All descriptions must be in Portuguese (pt-BR).

Document:
{text}

Return ONLY the JSON object, no other text."""
```

**Análise**:
1. **Estrutura JSON**: Define exatamente o formato esperado
2. **Campos**: parties, dates, values, clauses
3. **Tipos**: Enum de valores permitidos para cada campo
4. **Regras**: 5 regras específicas
5. **Instrução final**: "Return ONLY the JSON object" — força formato estruturado

### Prompt de Resumo

**Localização**: `backend/app/legal_agent.py:122`

```python
summary = llm.invoke(f"Faça um resumo detalhado do seguinte documento legal em português (pt-BR):\n\n{text}")
```

**Análise**:
- Simples, sem estrutura JSON
- Apenas pede resumo detalhado
- Força idioma português

### Prompt de Comparação

**Localização**: `backend/app/legal_agent.py:221-231`

```python
prompt = f"""Compare estes dois documentos legais e forneça em português (pt-BR):
1. Similaridades entre eles
2. Diferenças entre eles
3. Um resumo da comparação

Documento A:
{text_a[:3000]}

Documento B:
{text_b[:3000]}
"""
```

**Análise**:
- Define 3 seções esperadas
- Limita texto a 3000 caracteres por documento (para não exceder token limit)
- Força idioma português

---

## 7. Automação Pós-Upload

### Fluxo

```
1. Usuário faz upload de contrato
   ↓
2. Backend cria documento no banco
   ↓
3. Backend cria AutomationRun com status PENDING
   ↓
4. Backend agenda BackgroundTask
   ↓
5. BackgroundTask executa run_post_upload_automation()
   ├─ DOCUMENT_PROCESSING (10%): Verificar documento existe
   ├─ SUMMARY (30-50%): Executar SummaryTool
   ├─ RISK_ANALYSIS (70-85%): Executar RiskAnalyzer
   ├─ WEBHOOK (90%): Enviar análise.completed event
   └─ COMPLETED (100%): Finalizar status
   ↓
6. Webhook enviado para n8n (se configurado)
   ↓
7. n8n pode enviar email/Slack/integração
```

### Webhook Payload

```json
{
  "event": "analysis.completed",
  "event_id": "uuid-v4",
  "timestamp": "2026-07-26T10:30:00Z",
  "document": {
    "id": "doc-uuid",
    "title": "Contrato de Prestação de Serviços"
  },
  "automation": {
    "run_id": "run-uuid",
    "status": "COMPLETED"
  },
  "analysis": {
    "summary_available": true,
    "risk_analysis_available": true,
    "overall_risk": "high",
    "confidence_score": 85
  }
}
```

### Configuração

```bash
# .env
AUTOMATION_WEBHOOK_ENABLED=true
AUTOMATION_WEBHOOK_URL=https://n8n.example.com/webhook/legal-ai
AUTOMATION_WEBHOOK_TIMEOUT_SECONDS=10
AUTOMATION_WEBHOOK_MAX_RETRIES=3
```

---

## 8. Banco de Dados — Schema Completo

### Tabelas Principais

#### users
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,  -- ADMIN, LAWYER, ASSISTANT, CLIENT, VIEWER
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

#### documents
```sql
CREATE TABLE documents (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    filename VARCHAR(255),
    file_path VARCHAR(500),
    status VARCHAR(50),  -- uploading, ready, processing, failed
    page_count INTEGER,
    user_id VARCHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### chunks
```sql
CREATE TABLE chunks (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    chunk_index INTEGER,
    text LONGTEXT NOT NULL,
    page_number INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

#### document_embeddings
```sql
CREATE TABLE document_embeddings (
    id VARCHAR(36) PRIMARY KEY,
    chunk_id VARCHAR(36) NOT NULL,
    document_id VARCHAR(36) NOT NULL,
    embedding BLOB NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (chunk_id) REFERENCES chunks(id),
    FOREIGN KEY (document_id) REFERENCES documents(id)
);
```

#### conversations
```sql
CREATE TABLE conversations (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36),
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

#### messages
```sql
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    conversation_id VARCHAR(36) NOT NULL,
    content LONGTEXT NOT NULL,
    role VARCHAR(50),  -- user, assistant
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

#### analysis_records
```sql
CREATE TABLE analysis_records (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    analysis_type VARCHAR(50),  -- SUMMARY, EXTRACTION, COMPARISON, QUESTION_ANSWERING, RISK_ANALYSIS
    status VARCHAR(50),  -- GENERATED, PENDING_REVIEW, APPROVED, REJECTED, NEEDS_CHANGES
    content_summary VARCHAR(500),
    structured_result LONGTEXT,  -- JSON
    confidence_score INTEGER,
    confidence_level VARCHAR(50),  -- HIGH, MODERATE, LOW
    overall_risk VARCHAR(50),  -- low, medium, high, critical
    citations LONGTEXT,  -- JSON array
    disclaimer LONGTEXT,
    model_name VARCHAR(100),
    prompt_version VARCHAR(50),
    blocked BOOLEAN DEFAULT FALSE,
    estimated_manual_minutes INTEGER,
    estimated_time_saved_minutes INTEGER,
    version INTEGER DEFAULT 1,
    parent_analysis_id VARCHAR(36),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_analysis_id) REFERENCES analysis_records(id)
);
```

#### analysis_reviews
```sql
CREATE TABLE analysis_reviews (
    id VARCHAR(36) PRIMARY KEY,
    analysis_record_id VARCHAR(36) NOT NULL,
    reviewer_user_id VARCHAR(36) NOT NULL,
    previous_status VARCHAR(50),
    new_status VARCHAR(50),
    decision VARCHAR(50),  -- APPROVE, REJECT, REQUEST_CHANGES
    comment LONGTEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_record_id) REFERENCES analysis_records(id),
    FOREIGN KEY (reviewer_user_id) REFERENCES users(id)
);
```

#### automation_runs
```sql
CREATE TABLE automation_runs (
    id VARCHAR(36) PRIMARY KEY,
    document_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    automation_type VARCHAR(50),  -- post_upload
    status VARCHAR(50),  -- PENDING, RUNNING, COMPLETED, FAILED, PARTIAL_SUCCESS
    current_step VARCHAR(50),  -- DOCUMENT_PROCESSING, SUMMARY, RISK_ANALYSIS, WEBHOOK, COMPLETED
    progress_percent INTEGER,
    started_at DATETIME,
    completed_at DATETIME,
    error_message LONGTEXT,
    summary_result LONGTEXT,  -- JSON
    risk_result LONGTEXT,  -- JSON
    webhook_status VARCHAR(50),  -- pending, sent, failed
    webhook_error LONGTEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 9. Testes Automatizados

### Cobertura

```
Total: 166 testes
Status: ✅ TODOS PASSANDO

Distribuição:
- test_auth.py: 4 testes (JWT, expiração, validação)
- test_validators.py: 11 testes (validação de respostas)
- test_api.py: 8 testes (endpoints)
- test_agent_router.py: 10 testes (roteamento de intenção)
- test_agent_chat_integration.py: 15 testes (chat com RAG)
- test_risk_analysis.py: 20 testes (análise de riscos)
- test_ai_validator.py: 25 testes (guardrails)
- test_automation.py: 30 testes (automação pós-upload)
- test_analysis_review.py: 22 testes (revisão humana)
- test_demo_smoke.py: 21 testes (fluxo completo)
```

### Executar Testes

```bash
cd backend
source venv/bin/activate
ENVIRONMENT=testing python -m pytest -v

# Resultado esperado
# ===================== 166 passed in 38.42s =====================
```

---

## 10. Limitações Conhecidas e Evoluções Propostas

### Limitação 1: Sem OCR

**Atual**: Apenas PDFs digitalizados (texto extraível)

**Evolução**: Integrar Tesseract ou AWS Textract para PDFs digitalizados (imagens)

**Impacto**: Permitir análise de documentos escaneados

### Limitação 2: Análise de Riscos Determinística

**Atual**: Baseada em palavras-chave

**Evolução**: Usar LLM para análise semântica de riscos

**Impacto**: Detectar riscos mais sutis que não têm palavras-chave óbvias

### Limitação 3: SQLite Não-Escalável

**Atual**: SQLite para MVP

**Evolução**: PostgreSQL com pgvector para produção

**Impacto**: Suportar múltiplos usuários simultâneos, melhor performance

### Limitação 4: Sem Busca Híbrida

**Atual**: Apenas busca semântica

**Evolução**: Combinar busca semântica com busca por palavras-chave

**Impacto**: Melhor precisão em buscas específicas (ex: "cláusula 5")

### Limitação 5: Sem Reranking

**Atual**: Top-5 chunks por similaridade

**Evolução**: Usar modelo de reranking para reordenar resultados

**Impacto**: Melhor qualidade dos chunks recuperados

### Limitação 6: Sem Integração com Sistemas Jurídicos

**Atual**: Sistema standalone

**Evolução**: APIs para integração com Salesforce, SAP, etc.

**Impacto**: Integração com fluxos jurídicos existentes

### Limitação 7: Métricas Não-Calibradas

**Atual**: Estimativas do MVP

**Evolução**: Calibrar com dados reais de usuários

**Impacto**: Métricas precisas de impacto

### Limitação 8: Sem Refresh Token Auto-Refresh

**Atual**: Redirect para login em 401

**Evolução**: Silent refresh com refresh token

**Impacto**: Melhor UX (usuário não precisa fazer login novamente)

---

## 11. Segurança — Detalhamento

### Autenticação

**Tipo**: JWT (JSON Web Tokens)

**Fluxo**:
1. Usuário faz login com email e senha
2. Backend verifica credenciais (hash Argon2)
3. Backend gera access token (30 minutos) e refresh token (7 dias)
4. Frontend armazena tokens em localStorage
5. Frontend envia access token em Authorization header
6. Backend valida token em cada requisição

**Segurança**:
- ✅ Senhas com hash Argon2 (não reversível)
- ✅ Tokens com expiração
- ✅ Refresh token para renovação
- ❌ localStorage vulnerável a XSS (aceitável para MVP)

### RBAC (Role-Based Access Control)

**Papéis**:
- **ADMIN**: Acesso total
- **LAWYER**: Pode revisar análises, ver próprios documentos
- **ASSISTANT**: Pode ver documentos, não pode revisar
- **CLIENT**: Pode ver próprios documentos
- **VIEWER**: Acesso somente leitura

**Implementação**:
```python
@require_role(UserRole.LAWYER, UserRole.ADMIN)
def create_review(analysis_id: str, decision: str):
    # Apenas LAWYER e ADMIN podem revisar
    pass
```

### Ownership Enforcement

**Regra**: Usuário só acessa seus próprios documentos (exceto ADMIN)

```python
if current_user.role != UserRole.ADMIN and document.user_id != current_user.id:
    raise HTTPException(status_code=403, detail="Access denied")
```

### Logging Seguro

**O que é registrado**:
- ✅ Tipo de operação (upload, chat, análise)
- ✅ Timestamp
- ✅ Duração
- ✅ Resultado (sucesso/erro)
- ✅ User ID (anônimo)

**O que NÃO é registrado**:
- ❌ Conteúdo integral do documento
- ❌ Tokens JWT
- ❌ Senhas
- ❌ Authorization headers
- ❌ Pergunta integral sensível
- ❌ Resposta integral sensível

---

## 12. Performance — Benchmarks

### Tempos Típicos

| Operação | Tempo | Notas |
|----------|-------|-------|
| Upload de PDF (10 páginas) | 2-3s | Inclui extração, chunking, embeddings |
| Chat com RAG | 3-5s | Inclui busca semântica e LLM |
| Resumo | 3-5s | Apenas LLM |
| Extração | 4-6s | LLM + parsing JSON |
| Comparação | 5-8s | Dois documentos + LLM |
| Análise de riscos | 1-2s | Determinística, sem LLM |

### Fatores que Afetam Performance

1. **Tamanho do documento**: Documentos maiores = mais chunks = mais tempo
2. **Latência da API OpenAI**: Varia de 1-3 segundos
3. **Tamanho do contexto**: Mais chunks = mais tokens = mais tempo
4. **Carga do servidor**: Múltiplas requisições simultâneas

### Otimizações Recomendadas

1. **Cache de embeddings**: Não regenerar embeddings para documentos já processados
2. **Processamento assíncrono**: Não bloquear usuário durante análises longas
3. **Compressão de contexto**: Resumir chunks antes de enviar ao LLM
4. **Batch processing**: Processar múltiplos documentos em paralelo

---

## 13. Custo Estimado

### Custos Mensais (1000 contratos/mês)

| Serviço | Custo | Cálculo |
|---------|-------|---------|
| Embeddings | $0.30 | 1000 contratos × 30 chunks × $0.00001 |
| GPT-4o (chat) | $5.00 | 1000 chats × 2000 tokens × $0.0000025 |
| GPT-4o (resumo) | $3.00 | 1000 resumos × 1500 tokens × $0.0000020 |
| GPT-4o (extração) | $4.00 | 1000 extrações × 2000 tokens × $0.0000020 |
| GPT-4o (comparação) | $2.00 | 200 comparações × 5000 tokens × $0.0000020 |
| **Total OpenAI** | **$14.30** | |
| PostgreSQL (Heroku) | $50.00 | Dyno Standard |
| Armazenamento (S3) | $10.00 | 100 GB × $0.10 |
| **Total Mensal** | **$74.30** | |

### Custo por Contrato

```
$74.30 / 1000 = $0.07 por contrato
```

---

Fim dos detalhes técnicos complementares.
