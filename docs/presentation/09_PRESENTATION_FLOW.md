# Fluxo de Apresentação — Legal AI Copilot

> Resumo executivo de uma página. Visão geral do fluxo completo do vídeo.

---

## Visão Geral

**Projeto**: Legal AI Copilot — MVP de IA para análise de contratos jurídicos
**Duração**: 12–15 minutos
**Formato**: Screencast com narração (webcam opcional para abertura/encerramento)
**Stack**: FastAPI, React, TypeScript, SQLAlchemy, SQLite, JWT, RBAC

---

## Fluxo (14 Cenas)

```
[01] Abertura → [02] Problema → [03] Arquitetura
  ↓
[04] Login → [05] Dashboard → [06] Upload
  ↓
[07] Análise (resumo + extração) → [08] Chat (agent router + guardrails)
  ↓
[09] Riscos (heurística) → [10] Automações (pipeline + webhook)
  ↓
[11] Revisões (state machine + append-only) → [12] Métricas (estimativas)
  ↓
[13] Comparação → [14] Encerramento (limitações)
```

---

## Funcionalidades Demonstradas

| # | Funcionalidade | Tela | Tempo |
|---|---------------|------|-------|
| 1 | Autenticação JWT + RBAC | `/login` | 30s |
| 2 | Lista de documentos + navegação | `/dashboard` | 30s |
| 3 | Upload com processamento automático | `/upload` | 60s |
| 4 | Resumo + extração estruturada | `/analysis` | 90s |
| 5 | Chat com agent router determinístico | `/chat` | 90s |
| 6 | Análise de riscos heurística | `/risks` | 90s |
| 7 | Automação pós-upload + webhook | `/automations` | 45s |
| 8 | Revisão humana com state machine | `/reviews` | 60s |
| 9 | Métricas de impacto | `/insights` | 45s |
| 10 | Comparação de contratos | `/comparison` | 30s |

---

## Mensagens-Chave por Bloco

| Bloco | Mensagem |
|-------|----------|
| Abertura (01–03) | MVP funcional, stack moderna, arquitetura com guardrails |
| Demo principal (04–09) | Upload → processamento → análise → chat → riscos, tudo automatizado com guardrails |
| Workflow (10–11) | Automação em background + revisão humana com trilha de auditoria |
| Métricas (12) | Estimativas de produtividade transparentes |
| Comparação (13) | Análise lado a lado de dois contratos |
| Encerramento (14) | Limitações honestas: heurística sem LLM, SQLite, sem OCR, métricas estimadas |

---

## Limitações a Mencionar

- Análise de riscos: heurística (palavras-chave), sem LLM
- Similarity score: fixo (0.7), não calculado por embeddings
- Sem OCR (apenas extração de texto PDF)
- SQLite (adequado para MVP, PostgreSQL recomendado para produção)
- Métricas: estimativas do MVP, não calibradas
- Sem auto-refresh do JWT (redirect para login em 401)
- Funciona em modo heurístico sem OpenAI API key

---

## Credenciais Demo

| Perfil | Email | Senha |
|--------|-------|-------|
| Advogado | `lawyer@demo.com` | `demo123456` |
| Admin | `admin@demo.com` | `admin123456` |

---

## URLs da Aplicação

| Serviço | URL |
|---------|-----|
| Frontend | `http://localhost:5173` |
| Backend (API) | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |

---

## Arquivos de Documentação

| Arquivo | Conteúdo |
|---------|----------|
| `01_SCREEN_RECORDING_GUIDE.md` | Configuração técnica de captura, OBS, microfone |
| `02_DEMO_TIMELINE.md` | Cronograma minuto a minuto |
| `03_SCREEN_NAVIGATION_SCRIPT.md` | Cena por cena: ações, URLs, botões, resultados |
| `04_VIDEO_SPEECH_SCRIPT.md` | Roteiro de fala sincronizado com cenas |
| `05_CAMERA_NOTES.md` | Tom, pausas, ênfase, linguagem corporal |
| `06_RECORDING_CHECKLIST.md` | Checklist antes, durante, depois |
| `07_SCENE_RETAKE_GUIDE.md` | Regravação com continuidade |
| `08_DEMO_DATA_GUIDE.md` | Preparação de dados de demonstração |
| `09_PRESENTATION_FLOW.md` | Este resumo executivo |
