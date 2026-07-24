# Guardrails e Controle de Alucinações

## Visão Geral

O sistema implementa uma camada centralizada de validação de respostas jurídicas geradas por IA. O objetivo é:

1. **Bloquear alucinações** - Respostas sem evidência documental
2. **Quantificar confiança** - Score determinístico baseado em evidências reais
3. **Estruturar citações** - Rastreabilidade completa das fontes
4. **Avisar usuários** - Disclaimer jurídico obrigatório

---

## Arquitetura

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│ Endpoint (Chat, Resumo, Extração, Comparação)              │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ LLM / Legal Agent (Gera resposta)                           │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ AIValidator (app/ai_validator.py)                           │
│                                                              │
│ 1. Recupera chunks do documento                             │
│ 2. Valida resposta contra evidências                        │
│ 3. Calcula score de confiança                               │
│ 4. Estrutura citações                                       │
│ 5. Bloqueia se necessário                                   │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ ValidatedAIResponse (com metadados)                         │
│ - content (vazio se bloqueado)                              │
│ - validation (score, confiança, razões)                     │
│ - citations (estruturadas)                                  │
│ - blocked (true/false)                                      │
│ - block_reason (se bloqueado)                               │
└─────────────────────────────────────────────────────────────┘
```

### Fluxo de Validação

```
Pergunta do usuário
    ↓
Recuperação RAG (chunks)
    ↓
Geração da resposta (LLM)
    ↓
Extração de citações
    ↓
Validação de Evidências
    ├─ Existem chunks?
    ├─ Existem citações?
    ├─ Similaridade adequada?
    └─ Resposta sustentada?
    ↓
Cálculo de Score (0-100)
    ↓
Decisão de Bloqueio
    ├─ Score < 60? → BLOQUEADO
    └─ Score ≥ 60? → PERMITIDO
    ↓
Resposta Final com Metadados
```

---

## Fórmula do Score de Confiança

**Intervalo:** 0-100

**Composição:**

| Componente | Pontos | Critério |
|---|---|---|
| **Fontes** | até 30 | Quantidade e existência de chunks recuperados |
| **Similaridade** | até 30 | Score médio de similaridade dos chunks |
| **Citações** | até 20 | Quantidade e cobertura de citações |
| **Consistência** | até 10 | Alinhamento entre resposta e contexto |
| **Qualidade** | até 10 | Completude e significância do contexto |

**Detalhamento:**

### 1. Fontes (até 30 pontos)
- 0 chunks: 0 pontos
- 1 chunk: 10 pontos
- 2-3 chunks: 20 pontos
- 4+ chunks: 30 pontos

### 2. Similaridade (até 30 pontos)
- Média ≥ 0.80: 30 pontos
- Média 0.60-0.79: 20 pontos
- Média 0.30-0.59: 10 pontos
- Média < 0.30: 0 pontos

### 3. Citações (até 20 pontos)
- 3+ citações: 20 pontos
- 1-2 citações: 10 pontos
- 0 citações: 0 pontos

### 4. Consistência (até 10 pontos)
- Boas fontes (≥20) + boas citações (≥10): 10 pontos
- Caso contrário: 0 pontos

### 5. Qualidade (até 10 pontos)
- 80%+ chunks com conteúdo significativo (>50 chars): 10 pontos
- Alguns chunks significativos: 5 pontos
- Nenhum chunk significativo: 0 pontos

---

## Classificação de Confiança

| Score | Nível | Significado |
|---|---|---|
| 80-100 | **HIGH** | Forte sustentação documental |
| 60-79 | **MODERATE** | Evidência adequada com algumas lacunas |
| 0-59 | **LOW** | Evidência insuficiente |

**Importante:** O score é apresentado como **"nível de sustentação documental"**, não como probabilidade matemática de correção.

---

## Thresholds Configuráveis

Definidos em `app/config.py` e `.env`:

```python
MIN_SIMILARITY_SCORE = 0.3      # Mínimo para considerar chunk relevante
MIN_CONFIDENCE_SCORE = 60       # Mínimo para permitir resposta
MIN_CITATIONS = 1               # Mínimo de citações obrigatórias
MAX_CITATION_EXCERPT_LENGTH = 300  # Máximo de caracteres em excerpt
```

**Variáveis de Ambiente:**
```bash
MIN_SIMILARITY_SCORE=0.3
MIN_CONFIDENCE_SCORE=60
MIN_CITATIONS=1
MAX_CITATION_EXCERPT_LENGTH=300
```

---

## Regras de Bloqueio

Uma resposta é **BLOQUEADA** quando:

1. **Resposta vazia** - LLM retornou conteúdo vazio ou inválido
2. **Sem chunks** - Nenhum documento foi recuperado
3. **Sem citações** - Nenhuma citação foi extraída
4. **Baixa similaridade** - Todos os chunks têm score < MIN_SIMILARITY_SCORE
5. **Score insuficiente** - Confidence score < MIN_CONFIDENCE_SCORE
6. **Contexto vazio** - Chunks recuperados não contêm texto

**Mensagem Padrão:**
```
"Não encontrei evidências suficientes nos documentos selecionados para responder com segurança."
```

---

## Estrutura de Citações

### CitationSource

```python
@dataclass
class CitationSource:
    document_id: str              # ID do documento
    document_title: str           # Título do documento
    chunk_id: str                 # ID do chunk
    page_number: Optional[int]    # Número da página (se disponível)
    excerpt: str                  # Trecho do texto (até 300 chars)
    similarity_score: Optional[float]  # Score de similaridade (0-1)
```

### Processamento

- **Deduplicação:** Citações duplicadas são removidas
- **Truncamento:** Excerpts maiores que MAX_CITATION_EXCERPT_LENGTH são truncados com "..."
- **Ordenação:** Citações são ordenadas por relevância (similarity_score desc)
- **Validação:** Página não é inventada; permanece null se não disponível

---

## Disclaimer Jurídico

**Texto Obrigatório:**
```
"Esta análise foi gerada com auxílio de inteligência artificial, 
com base nos documentos fornecidos, e não substitui a revisão de um profissional jurídico."
```

**Centralizado em:** `AIValidator.LEGAL_DISCLAIMER`

**Presente em:** Todas as respostas validadas, mesmo as bloqueadas

---

## Integração com Endpoints

### Chat com RAG
- ✅ Validação completa implementada
- ✅ Score, citações e disclaimer retornados
- ✅ Respostas bloqueadas não expõem conteúdo inseguro

### Resumo
- Validação mínima (documento existe?)
- Não passa por AIValidator; usa LLM (GPT-4o) diretamente

### Extração
- Validação mínima (campos encontrados?)
- Não passa por AIValidator; usa LLM (GPT-4o) com prompt estruturado

### Comparação
- Validação mínima (documentos existem?)
- Não passa por AIValidator; usa LLM (GPT-4o) diretamente

### Análise de Riscos
- Não usa LLM nem AIValidator
- Análise heurística determinística (palavras-chave)
- Confidence score calculado por fórmula própria (não pelo AIValidator)

---

## Exemplos

### Exemplo 1: Alta Confiança (Score 85)

**Entrada:**
```
Pergunta: "Qual é o valor do contrato?"
Chunks: 3 recuperados, similaridade média 0.87
Citações: 2 extraídas
```

**Saída:**
```json
{
  "content": "O valor total do contrato é de R$ 50.000,00, conforme cláusula 2.1.",
  "validation": {
    "confidence_score": 85,
    "confidence_level": "high",
    "evidence_sufficient": true,
    "hallucination_risk": "LOW",
    "validation_reasons": [
      "Três fontes recuperadas (múltiplas)",
      "Similaridade alta (média: 0.87)",
      "Cobertura de citações completa (2 citações)",
      "Consistência entre resposta e contexto",
      "Qualidade de contexto adequada"
    ],
    "citations": [
      {
        "document_id": "doc1",
        "document_title": "Contrato de Prestação de Serviços",
        "chunk_id": "chunk5",
        "page_number": 2,
        "excerpt": "O valor total do contrato é de R$ 50.000,00...",
        "similarity_score": 0.92
      }
    ],
    "disclaimer": "Esta análise foi gerada com auxílio de inteligência artificial..."
  },
  "blocked": false
}
```

### Exemplo 2: Confiança Moderada (Score 68)

**Entrada:**
```
Pergunta: "Quais são as cláusulas de rescisão?"
Chunks: 1 recuperado, similaridade 0.65
Citações: 1 extraída
```

**Saída:**
```json
{
  "content": "O contrato prevê rescisão por acordo mútuo conforme cláusula 5.2.",
  "validation": {
    "confidence_score": 68,
    "confidence_level": "moderate",
    "evidence_sufficient": true,
    "hallucination_risk": "MEDIUM",
    "validation_reasons": [
      "Uma fonte recuperada",
      "Similaridade moderada (média: 0.65)",
      "Cobertura de citações parcial (1 citação(ões))"
    ],
    "citations": [
      {
        "document_id": "doc1",
        "document_title": "Contrato de Prestação de Serviços",
        "chunk_id": "chunk12",
        "page_number": 4,
        "excerpt": "Rescisão por acordo mútuo...",
        "similarity_score": 0.65
      }
    ],
    "disclaimer": "Esta análise foi gerada com auxílio de inteligência artificial..."
  },
  "blocked": false
}
```

### Exemplo 3: Resposta Bloqueada (Score 35)

**Entrada:**
```
Pergunta: "Qual é a taxa de juros?"
Chunks: 0 recuperados
Citações: 0 extraídas
```

**Saída:**
```json
{
  "content": "",
  "validation": {
    "confidence_score": 0,
    "confidence_level": "low",
    "evidence_sufficient": false,
    "hallucination_risk": "HIGH",
    "validation_reasons": [
      "Nenhuma fonte recuperada",
      "Nenhuma citação fornecida"
    ],
    "citations": [],
    "disclaimer": "Esta análise foi gerada com auxílio de inteligência artificial..."
  },
  "blocked": true,
  "block_reason": "Não encontrei evidências suficientes nos documentos selecionados para responder com segurança."
}
```

---

## Logging

### Eventos Registrados

```python
logger.info("Validation started", extra={
    "conversation_id": "conv123",
    "document_id": "doc1",
    "user_id": "user1"
})

logger.info("Validation completed", extra={
    "confidence_score": 85,
    "confidence_level": "high",
    "citation_count": 2,
    "average_similarity": 0.87,
    "duration_ms": 245
})

logger.warning("Validation blocked", extra={
    "confidence_score": 35,
    "block_reason": "no_chunks",
    "duration_ms": 120
})
```

### Dados NÃO Registrados

- ❌ Conteúdo integral do documento
- ❌ Tokens JWT
- ❌ Senhas
- ❌ Authorization headers
- ❌ Pergunta integral sensível
- ❌ Resposta integral sensível

---

## Limitações Conhecidas

1. **Sem validação por LLM** - Primeira versão usa apenas validação determinística
2. **Sem análise semântica avançada** - Usa similaridade de embeddings
3. **Sem detecção de contradição** - Não identifica respostas contraditórias
4. **Sem análise de completude** - Não verifica se resposta é completa
5. **Sem cache de validação** - Cada resposta é validada novamente

---

## Próximas Etapas

- [ ] Integrar AIValidator em Resumo, Extração e Comparação
- [ ] Implementar validação por LLM (opcional)
- [ ] Adicionar análise de contradição
- [ ] Implementar cache de validação
- [ ] Dashboard de confiança

---

## Referências

- `app/ai_validator.py` - Implementação do validador
- `tests/test_ai_validator.py` - Testes unitários
- `app/main.py` - Integração com endpoints
- `app/config.py` - Configuração de thresholds
