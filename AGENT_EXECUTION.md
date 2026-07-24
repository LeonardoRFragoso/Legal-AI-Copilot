# Agent Execution and Chat Integration

## Overview

The Agent Router is integrated into the chat flow, replacing direct `legal_agent.query()` calls with deterministic intent classification and tool execution.

## Architecture

```
User Message -> Agent Router (deterministic) -> Agent Executor -> Tool Execution -> Validation -> Response
```

### Key Components

- **`app/agent_router.py`**: Deterministic router with keyword heuristics
- **`app/agent_executor.py`**: Reusable execution service for tool execution
- **`app/main.py`**: Chat endpoint uses router + executor

## Supported Intents

| Intent | Tool | Trigger Keywords |
|--------|------|-----------------|
| SUMMARIZE_DOCUMENT | summarize_document | resumo, resumir, summarize |
| EXTRACT_INFORMATION | extract_information | extrair, extraia, extract, partes |
| COMPARE_DOCUMENTS | compare_documents | comparar, compare, diferenças |
| IDENTIFY_RISKS | contract_risk_analysis | riscos, risco, risk, perigos |
| QUESTION_ANSWERING | semantic_search | qual, o que, quando, how, what |
| UNKNOWN | unknown | (fallback) |

## Chat Flow

1. User sends message to `/conversations/{conversation_id}/messages`
2. Agent Router classifies intent using keyword heuristics
3. Agent Executor validates document access (ownership + RBAC)
4. Appropriate tool is executed in-process
5. For QUESTION_ANSWERING, response is validated through AIValidator guardrails
6. Result is persisted as assistant message with agent metadata

## Agent Metadata in Messages

Assistant messages include structured metadata in the `citations` JSON field:

- `agent`: intent, tool, blocked flag
- `citations`: array of citation sources
- `validation`: confidence score, hallucination risk, blocked status
- `structured_data`: extracted data for EXTRACT_INFORMATION and IDENTIFY_RISKS
- `disclaimer`: legal disclaimer text

## Security

- **Ownership validation**: Document access checked before tool execution
- **RBAC**: ADMIN sees all; other roles only their own documents
- **Guardrails**: AIValidator validates responses for QUESTION_ANSWERING
- **No chain-of-thought**: Router decisions contain only short, safe reasons

## Testing

Tests in `tests/test_agent_chat_integration.py` cover:
- Intent classification for each intent type via chat
- Document ownership enforcement (403 for other users' documents)
- Blocked content not exposed
- No chain-of-thought in router decisions
