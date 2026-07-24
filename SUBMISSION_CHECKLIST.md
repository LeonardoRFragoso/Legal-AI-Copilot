# Checklist de Entrega — Legal AI Copilot

## Documentos

- [ ] `CASE_FINAL_PDF_CONTENT.md` — conteúdo do PDF (5 páginas)
- [ ] `CASE_FINAL_ANSWERS.md` — respostas às 7 perguntas do case
- [ ] `DEMO_SCRIPT_FINAL.md` — roteiro do vídeo (7-9 min)
- [ ] `VIDEO_SPEECH_SCRIPT.md` — script de fala em português
- [ ] `RECORDING_CHECKLIST.md` — checklist pré-gravação
- [ ] `SUBMISSION_CHECKLIST.md` — este arquivo
- [ ] `INTERVIEW_QUICK_REFERENCE.md` — respostas rápidas para entrevista
- [ ] `FINAL_DELIVERY_REPORT.md` — relatório final de entrega

## PDF

- [ ] HTML A4 gerado (`deliverables/legal_ai_copilot_case.html`)
- [ ] PDF gerado a partir do HTML OU limitação documentada
- [ ] PDF com no máximo 5 páginas
- [ ] Texto não cortado nas margens
- [ ] Links legíveis
- [ ] Caracteres portugueses (ã, ç, é) renderizados corretamente
- [ ] Sem páginas em branco

## Vídeo

- [ ] Duração entre 7 e 9 minutos
- [ ] Áudio legível e sem ruídos
- [ ] Tela legível (zoom adequado)
- [ ] Sem dados pessoais visíveis
- [ ] Sem senhas visíveis (usar autofill demo)
- [ ] Fluxo completo demonstrado (login → upload → chat → riscos → revisão → métricas)

## GitHub

- [ ] Repositório público ou acessível: https://github.com/LeonardoRFragoso/Legal-AI-Copilot
- [ ] README.md atualizado e correto
- [ ] Commit final realizado
- [ ] Push confirmado
- [ ] Sem secrets no repositório (verificar `.env`, API keys, tokens)
- [ ] Sem arquivos de banco de dados versionados
- [ ] Sem `node_modules` versionados

## Testes e Build

- [ ] `pytest -q` — 166 passed, 0 failed
- [ ] `npm run build` — PASS (tsc + vite)
- [ ] `git diff --check` — sem erros de whitespace

## Variáveis de Ambiente

- [ ] `.env.example` do backend completo e sem secrets
- [ ] `.env.example` do frontend completo e sem secrets
- [ ] `.env` em `.gitignore` (backend e frontend)
- [ ] Nenhum valor real de API key no código ou documentação

## Conferência Final

- [ ] Ortografia revisada em todos os documentos
- [ ] Número de testes consistente (166) em todos os documentos
- [ ] Nomes de tecnologias corretos (FastAPI, LangChain, GPT-4o, etc.)
- [ ] Nomes de endpoints corretos (/analyses, /metrics/impact, etc.)
- [ ] Limitações listadas corretamente (sem LLM em risco, sem OCR, etc.)
- [ ] Métricas descritas como estimativas do MVP
- [ ] Análise de riscos descrita como heurística, não RAG/LLM
- [ ] n8n descrito como workflow de exemplo, não executado em produção
- [ ] similarity_score descrito como fixo ilustrativo (0.7)
- [ ] Duração do roteiro entre 7 e 9 minutos
