# Phase 2 — Stage 5 Precheck

**Commit inicial**: fab073151baeda8b649bdb3b30751a3834f7295c
**Branch**: main
**Data**: 2026-07-24

## Estado do Git

- Branch: `main`
- HEAD: `fab0731` (igual ao remote `origin/main`)
- Status: clean (nenhuma alteração não commitada)
- `git pull`: Already up to date

## Ambiente

- Python 3.12 (venv em `backend/venv/`)
- Node.js + npm (frontend)
- SQLite (banco de teste: `test_shared.db`)
- ENVIRONMENT=testing para pytest

## Suíte de Testes — Resultado Inicial

```
9 failed, 149 passed, 591 warnings, 18.49s
```

### Testes Falhos

#### test_api.py (6 falhas)

1. **test_api.py::TestDocumentEndpoints::test_list_documents**
   - Esperado: 200 (lista de documentos)
   - Atual: 401 Unauthorized
   - Causa raiz: Endpoint `/documents` exige `get_current_user` (JWT), mas o teste não envia token de autenticação.

2. **test_api.py::TestDocumentEndpoints::test_get_nonexistent_document**
   - Esperado: 404 ou 500
   - Atual: 401 Unauthorized
   - Causa raiz: Mesma — endpoint exige auth, teste não envia token.

3. **test_api.py::TestConversationEndpoints::test_list_conversations**
   - Esperado: 200 (lista de conversas)
   - Atual: 401 Unauthorized
   - Causa raiz: Mesma — endpoint exige auth.

4. **test_api.py::TestAnalysisEndpoints::test_summary_endpoint_exists**
   - Esperado: 200, 400, ou 500
   - Atual: 401 Unauthorized
   - Causa raiz: Mesma — endpoint exige auth.

5. **test_api.py::TestAnalysisEndpoints::test_extract_endpoint_exists**
   - Esperado: 200, 400, ou 500
   - Atual: 401 Unauthorized
   - Causa raiz: Mesma.

6. **test_api.py::TestAnalysisEndpoints::test_compare_endpoint_exists**
   - Esperado: 200, 400, ou 500
   - Atual: 401 Unauthorized
   - Causa raiz: Mesma.

#### test_validators.py (3 falhas)

7. **test_validators.py::TestExtractionValidator::test_empty_extraction**
   - Esperado: `valid: True`, `warnings > 0` para listas vazias
   - Atual: `warnings == 0` (falha na asserção de warnings)
   - Causa raiz: O código verifica `if data.get("parties") and len(data["parties"]) == 0` — uma lista vazia é falsy em Python, então `data.get("parties")` retorna `[]` que é falso, e a condição inteira é falsa. O warning nunca é adicionado.

8. **test_validators.py::TestSummaryValidator::test_short_summary**
   - Esperado: `valid: False` para resumo muito curto ("Curto", 5 chars)
   - Atual: `valid: True` (apenas warning, não error)
   - Causa raiz: O código adiciona apenas warning para `len(summary) < 50`, não error. O teste espera que resumos muito curtos sejam inválidos.

9. **test_validators.py::TestConfidenceValidator::test_uncertain_response**
   - Esperado: `valid: False`, `confidence_score < 0.7` para "Talvez seja assim, mas não tenho certeza."
   - Atual: `valid: True`, `confidence_score = 0.9`
   - Causa raiz: O validador itera indicadores em ordem de inserção do dict. "certeza" (0.9) aparece primeiro e corresponde em "não tenho certeza", definindo score=0.9 e interrompendo o loop. Indicadores de incerteza ("talvez", "não sei") nunca são verificados.

## Build Frontend

```
npm run build: ✓ built in 2.54s
- dist/index.html: 0.47 kB
- dist/assets/index-BWwv2_Zf.css: 20.02 kB
- dist/assets/index-FsNyrfUO.js: 305.28 kB
```

TypeScript compilation: PASS (via `tsc && vite build`)

## Lint Frontend

- `npm run lint`: Falha — ESLint não tem configuração (.eslintrc ausente)
- Não há script `test` ou `typecheck` separado
- Build (tsc) serve como verificação de tipos

## Migrations

```
alembic heads: b8678ebaa440 (single head)
alembic history:
  <base> -> 4f38586d77d6, add automation_runs table
  4f38586d77d6 -> b8678ebaa440 (head), add_analysis_records_and_reviews
```

Cadeia íntegra, sem conflito de heads.

## Riscos da Demonstração

1. **6 testes de API sem auth**: Testes não refletem arquitetura atual com auth obrigatória
2. **Validadores com bugs lógicos**: Extração vazia não gera warning; resumo curto não é invalidado; confiança incorreta para respostas ambíguas
3. **Sem smoke test integrado**: Não há teste end-to-end do fluxo de demo
4. **Sem script de reset de demo**: Demo manual sem reproduzibilidade
5. **Documento de teste**: PDF existe no repo mas não é versionado como fixture de teste
6. **Credenciais demo expostas no frontend**: Botões de demo sempre visíveis, mesmo em produção

## Plano de Correção

1. **test_api.py**: Adicionar fixtures de usuário autenticado (criar usuário, gerar token JWT, enviar headers)
2. **test_validators.py — empty_extraction**: Corrigir lógica de warning para listas vazias (`field in data and len(data[field]) == 0`)
3. **test_validators.py — short_summary**: Adicionar error para resumos muito curtos (< 10 chars)
4. **test_validators.py — uncertain_response**: Corrigir validador de confiança para usar score mais conservador quando múltiplos indicadores presentes
