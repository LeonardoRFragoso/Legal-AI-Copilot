# Contract Risk Analysis

## Visão Geral

O módulo de análise de riscos contratuais identifica potenciais problemas em contratos usando análise heurística determinística baseada em palavras-chave. Não utiliza LLM nem recuperação semântica por embeddings.

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│ POST /analysis/risks                                        │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ RiskAnalyzer (app/risk_analysis.py)                         │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Layer 1: HeuristicAnalyzer                              │ │
│ │ - Detecta cláusulas ausentes                            │ │
│ │ - Detecta padrões problemáticos                         │ │
│ │ - 100% determinístico                                   │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Layer 2: Text-based Retrieval                           │ │
│ │ - Recupera chunks relevantes por palavra-chave          │ │
│ │ - Busca textual (não semântica)                         │ │
│ │ - Usado apenas para gerar citações                     │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                              │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Layer 3: Validation & Scoring                           │ │
│ │ - Calcula overall_risk baseado nas heurísticas          │ │
│ │ - Calcula confidence_score                               │ │
│ │ - Aplica disclaimer jurídico                             │ │
│ └─────────────────────────────────────────────────────────┘ │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ RiskAnalysisResponse                                        │
│ - overall_risk (LOW/MEDIUM/HIGH/CRITICAL)                   │
│ - confidence_score (0-100)                                  │
│ - confidence_level (HIGH/MODERATE/LOW)                      │
│ - summary                                                   │
│ - risks[]                                                   │
│ - citations[]                                               │
│ - disclaimer                                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Agent Router

### Arquitetura

O `LegalAgentRouter` classifica a intenção do usuário usando heurísticas determinísticas.

```python
from app.agent_router import LegalAgentRouter, AgentIntent

router = LegalAgentRouter()
decision = router.route("quais são os riscos deste contrato?")
# → RouterDecision(
#     intent=AgentIntent.IDENTIFY_RISKS,
#     tool="contract_risk_analysis",
#     reason="User requested risk identification",
#     confidence=0.95
#   )
```

### Intents Suportadas

| Intent | Tool | Palavras-chave |
|---|---|---|
| `SUMMARIZE_DOCUMENT` | `summarize_document` | resumo, summary, resumir |
| `EXTRACT_INFORMATION` | `extract_information` | extrair, extract, partes, datas |
| `COMPARE_DOCUMENTS` | `compare_documents` | comparar, compare, diferença |
| `IDENTIFY_RISKS` | `contract_risk_analysis` | risco, risk, perigo, problema |
| `QUESTION_ANSWERING` | `semantic_search` | qual, quais, what, when |
| `UNKNOWN` | `unknown` | (nenhuma correspondência) |

### Decisão

O router retorna uma `RouterDecision` contendo:
- `intent`: Enum com a intenção identificada
- `tool`: Nome da ferramenta a executar
- `reason`: Razão da decisão (não expõe chain of thought)
- `required_documents`: Documentos necessários
- `confidence`: Confiança na decisão (0-1)

---

## Heurísticas Implementadas

### Cláusulas Ausentes

| Heurística | Severidade | Categoria | Detecção |
|---|---|---|---|
| Confidencialidade ausente | MEDIUM | Confidentiality | Sem keywords: confidencial, confidentiality, sigilo, nda |
| LGPD ausente | HIGH | LGPD | Sem keywords: lgpd, dados pessoais, privacidade |
| Rescisão ausente | MEDIUM | Termination | Sem keywords: rescisão, termination, encerramento |

### Padrões Problemáticos

| Heurística | Severidade | Categoria | Detecção |
|---|---|---|---|
| Multa ilimitada | CRITICAL | Penalty | Texto contém "multa ilimitada" ou "unlimited penalty" |
| Renovação automática | MEDIUM | Renewal | Texto contém "renovação automática" ou "automatic renewal" |
| Pagamento indefinido | HIGH | Payment | Texto contém "pagamento indefinido" ou "indefinite payment" |

---

## Severidade

| Nível | Valor | Significado |
|---|---|---|
| `LOW` | low | Risco menor, monitorar |
| `MEDIUM` | medium | Risco moderado, recomendar ação |
| `HIGH` | high | Risco significativo, ação necessária |
| `CRITICAL` | critical | Risco crítico, ação imediata |

## Categorias

- `Confidentiality` - Cláusulas de confidencialidade
- `LGPD` - Proteção de dados
- `Termination` - Rescisão contratual
- `Payment` - Termos de pagamento
- `Liability` - Responsabilidade civil
- `Penalty` - Multas e penalidades
- `Forum` - Cláusula de foro
- `SLA` - Acordos de nível de serviço
- `Intellectual Property` - Propriedade intelectual
- `Renewal` - Renovação
- `Duration` - Vigência
- `Compliance` - Conformidade
- `Other` - Outros

---

## Overall Risk

Calculado baseado na maior severidade encontrada:

```
se CRITICAL in risks → CRITICAL
else if HIGH in risks → HIGH
else if MEDIUM in risks → MEDIUM
else → LOW
```

---

## Confidence Score

Calculado baseado em:
- Número de riscos encontrados (até 20 pontos)
- Cobertura de chunks relevantes (até 30 pontos)
- Base de 50 pontos

---

## Integração com Guardrails

O módulo utiliza:
- `CitationSource` para citações estruturadas
- Disclaimer jurídico centralizado
- Confidence score com classificação HIGH/MODERATE/LOW

**Nota:** `AIValidator` é importado mas não utilizado na análise de riscos atual. A validação é feita apenas pelo cálculo determinístico de confidence score.

---

## Integração com Chat

Quando o usuário pergunta sobre riscos:

```
"quais riscos"
    ↓
Agent Router → IDENTIFY_RISKS
    ↓
Risk Analysis → Heurísticas + Text Search
    ↓
Guardrails → Validação
    ↓
Confidence Score → 0-100
    ↓
Structured Citations → Fontes
    ↓
Resposta
```

---

## Endpoint

### POST /analysis/risks

**Request:**
```json
{
  "document_id": "uuid"
}
```

**Response:**
```json
{
  "overall_risk": "high",
  "confidence_score": 75,
  "confidence_level": "moderate",
  "summary": "Found 3 risk(s). 1 high severity. Overall risk level: high.",
  "risks": [
    {
      "title": "Missing LGPD Compliance Clause",
      "description": "The contract does not reference LGPD compliance.",
      "severity": "high",
      "category": "lgpd",
      "recommendation": "Include LGPD compliance clause.",
      "citations": [],
      "confidence_score": 85
    }
  ],
  "citations": [
    {
      "document_id": "doc1",
      "document_title": "Contrato",
      "chunk_id": "chunk5",
      "page_number": 2,
      "excerpt": "...",
      "similarity_score": 0.7
    }
  ],
  "disclaimer": "Esta análise de riscos foi gerada com auxílio de inteligência artificial..."
}
```

---

## Frontend

### Página: /risks

- Seleção de documento
- Botão "Analyze Risks"
- Exibição de:
  - Overall Risk (badge colorido)
  - Confidence Score (porcentagem)
  - Summary
  - Lista de riscos com:
    - Severity badge
    - Category tag
    - Description
    - Recommendation
    - Sources expansíveis (página, excerpt, similaridade)
  - Disclaimer jurídico

---

## Limitações

1. **Heurísticas fixas** - Palavras-chave pré-definidas, não adaptativas
2. **Sem LLM** - A análise usa apenas heurísticas determinísticas; LLM não é utilizado
3. **Sem RAG semântico** - A recuperação de chunks é por busca textual (palavras-chave), não por embeddings semânticos
4. **Sem análise semântica profunda** - Não detecta contradições
5. **Sem detecção de foro** - Não implementado ainda
6. **Sem detecção de SLA** - Não implementado ainda
7. **Sem detecção de PI** - Não implementado ainda

---

## Testes

### Agent Router (25 testes)
- Detecção de todas as intents
- Casos em português e inglês
- Case insensitive
- Tratamento de whitespace
- Múltiplas keywords

### Risk Analysis (18 testes)
- Documento inexistente
- Documento vazio
- Contrato simples
- Contrato complexo
- Detecção de cláusulas ausentes
- Detecção de padrões problemáticos
- Cálculo de overall risk
- Cálculo de confidence score
- Geração de summary
- Conversão para dict

Todos os testes usam mocks e não requerem OpenAI.

**Nota sobre `similarity_score`:** O valor `0.7` exibido nas citações é um valor heurístico fixo, não calculado por similaridade semântica real.
