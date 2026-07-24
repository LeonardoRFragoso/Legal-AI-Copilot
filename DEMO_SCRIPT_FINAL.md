# Roteiro Final do Vídeo — Legal AI Copilot

**Duração alvo**: 7 a 9 minutos
**Formato**: Screencast com narração

---

## 0:00–0:30 — Apresentação e Contexto

**O que falar**: Nome, projeto, problema (revisão manual de contratos é lenta e repetitiva), objetivo (acelerar com IA mantendo humano no controle).

**Onde clicar**: Nenhum — tela de título ou slide de abertura.

**Mensagem principal**: "Este é o Legal AI Copilot, um MVP que combina IA, guardrails e revisão humana para análise de contratos."

**Risco de erro**: Nenhum.

**Plano alternativo**: N/A.

---

## 0:30–1:10 — Problema e Objetivo

**O que falar**: Escritórios gastam horas em revisão. O MVP demonstra resumo, extração, comparação, análise de riscos e Q&A com RAG. Tudo com revisão humana obrigatória.

**Onde clicar**: Nenhum — continuar em slide ou tela inicial.

**Mensagem principal**: "IA acelera, humano decide. Cada análise é revisável."

**Risco de erro**: Nenhum.

**Plano alternativo**: N/A.

---

## 1:10–2:00 — Arquitetura

**O que falar**: Stack FastAPI + React. Agent Router determinístico (sem LLM na decisão). GPT-4o para resumo, extração, comparação e Q&A. Análise de riscos é heurística (palavras-chave). Guardrails com AIValidator em Q&A. SQLite no MVP.

**Onde clicar**: Mostrar diagrama (slide ou README no GitHub).

**Mensagem principal**: "O Agent Router é determinístico — não consome tokens do LLM para decidir."

**Risco de erro**: Nenhum.

**Plano alternativo**: N/A.

---

## 2:00–2:40 — Login e RBAC

**O que falar**: Autenticação JWT com 5 papéis. Demo com LAWYER e ADMIN. Credenciais demo só aparecem em modo desenvolvimento.

**Onde clicar**:
1. Abrir http://localhost:5173
2. Tela de login aparece
3. Clicar em "Advogado" (autofill)
4. Clicar "Entrar"
5. Dashboard carrega com nome e role no header

**Mensagem principal**: "RBAC desde o login — cada papel tem permissões diferentes."

**Risco de erro**: Backend não rodando → tela de erro de conexão.

**Plano alternativo**: Ter backend já rodando antes de gravar. Se falhar, mostrar screenshot do login.

---

## 2:40–3:30 — Upload e Automação

**O que falar**: Upload de PDF. Extração de texto, chunking, embeddings. Automação pós-upload executa resumo e análise de riscos automaticamente. Webhook opcional para n8n.

**Onde clicar**:
1. Clicar "Upload" no menu
2. Preencher título: "Contrato de Prestação de Serviços"
3. Selecionar PDF de teste
4. Clicar "Fazer Upload"
5. Aguardar redirecionamento
6. Clicar "Automações" no menu
7. Mostrar AutomationRun com progresso e status

**Mensagem principal**: "Upload dispara automação — resumo e riscos prontos sem ação manual."

**Risco de erro**: PDF sem texto extraível → chunks vazios. OpenAI API key ausente → resumo retorna mensagem de erro.

**Plano alternativo**: Ter documento já uploadado e automação já concluída antes de gravar. Mostrar o resultado pronto.

---

## 3:30–4:20 — Resumo ou Q&A com RAG

**O que falar**: Chat com Agent Router. Demonstrar Q&A com RAG — pergunta sobre o contrato, resposta com citações e confidence score.

**Onde clicar**:
1. Clicar "Chat" no menu
2. Criar nova conversa ou selecionar existente
3. Selecionar documento
4. Digitar: "qual é o valor do contrato?"
5. Aguardar resposta
6. Mostrar resposta com citações e confidence score

**Mensagem principal**: "RAG recupera chunks relevantes por similaridade semântica e envia ao GPT-4o com contexto."

**Risco de erro**: Sem OpenAI API key → resposta de fallback. Sem embeddings → sem chunks recuperados.

**Plano alternativo**: Ter conversa já iniciada com resposta salva. Mostrar screenshot se API key não estiver configurada.

---

## 4:20–5:10 — Análise de Riscos Heurística

**O que falar**: Análise de riscos é determinística, baseada em palavras-chave. Detecta cláusulas ausentes (confidencialidade, LGPD, rescisão) e padrões problemáticos (multa ilimitada, renovação automática). Sem LLM.

**Onde clicar**:
1. Clicar "Riscos" no menu
2. Selecionar documento
3. Mostrar riscos identificados com severity badges
4. Destacar overall_risk e confidence score
5. Mostrar disclaimer jurídico

**Mensagem principal**: "Sem LLM aqui — heurística determinística. Rápido, gratuito e reproduzível."

**Risco de erro**: Documento sem chunks → "No content found". Riscos podem não aparecer se palavras-chave não corresponderem.

**Plano alternativo**: Usar documento sintético (`tests/fixtures/synthetic_contract.txt`) que contém todas as palavras-chave problemáticas.

---

## 5:10–6:00 — Guardrails, Citações e Confiança

**O que falar**: AIValidator em Q&A. Confidence score 0-100. Score < 60 bloqueia resposta. Citações estruturadas com page_number e excerpt. Disclaimer sempre presente.

**Onde clicar**:
1. Voltar ao Chat
2. Fazer pergunta irrelevante: "qual a taxa de juros?"
3. Mostrar resposta bloqueada
4. Voltar a pergunta relevante
5. Mostrar citações expansíveis

**Mensagem principal**: "Guardrails bloqueiam respostas sem evidência. O usuário nunca vê uma alucinação não fundamentada."

**Risco de erro**: Pergunta irrelevante pode não bloquear se houver chunks com similaridade baixa mas > 0.3.

**Plano alternativo**: Mostrar screenshot do exemplo de bloqueio (score 0) da documentação.

---

## 6:00–6:50 — Revisão Humana

**O que falar**: Toda análise é persistida como AnalysisRecord. State machine: GENERATED → PENDING_REVIEW → APPROVED/REJECTED. Histórico append-only. RBAC: LAWYER e ADMIN revisam.

**Onde clicar**:
1. Clicar "Revisões" no menu
2. Mostrar lista de análises com filtros
3. Clicar em uma análise
4. Mostrar detalhe com structured_data, confidence, disclaimer
5. Mover para PENDING_REVIEW (se necessário)
6. Clicar "Aprovar" com comentário
7. Mostrar histórico de revisão atualizado

**Mensagem principal**: "Humano no controle — nada é definitivo sem revisão."

**Risco de erro**: Análise já aprovada → não pode aprovar de novo. Análise bloqueada → não pode aprovar.

**Plano alternativo**: Ter análise já em PENDING_REVIEW antes de gravar.

---

## 6:50–7:30 — Métricas e Automações

**O que falar**: Dashboard de métricas com estimativas de tempo economizado. Valores configuráveis. Estimativas do MVP, não resultados reais. Automações com status e webhook.

**Onde clicar**:
1. Clicar "Métricas" no menu
2. Mostrar cards: documentos, análises, tempo economizado, taxa de aprovação
3. Mostrar breakdowns: análises por tipo, riscos por severidade
4. Mostrar aviso de estimativa
5. Clicar "Automações" no menu
6. Mostrar runs com status e progresso

**Mensagem principal**: "Métricas são estimativas do MVP — baseadas em tempos manuais configuráveis, não validadas em produção."

**Risco de erro**: Sem análises → dashboard vazio.

**Plano alternativo**: Ter dados de demo já carregados (executar demo_reset + upload antes).

---

## 7:30–8:10 — Segurança, Limitações e Próximos Passos

**O que falar**: JWT, Argon2, RBAC, ownership. Limitações: sem OCR, sem refresh auto, SQLite, BackgroundTasks sem fila. Próximos: PostgreSQL, Celery, AIValidator em todas as operações, RAG na análise de riscos.

**Onde clicar**:
1. Fazer logout
2. Mostrar tela de login
3. Opcional: login como ADMIN, mostrar system-status

**Mensagem principal**: "MVP funcional com limitações claras e plano de evolução definido."

**Risco de erro**: Nenhum.

**Plano alternativo**: N/A.

---

## 8:10–8:30 — Conclusão

**O que falar**: 166 testes, 0 falhas. Frontend compilando. Migrations validadas. Código no GitHub. Obrigado.

**Onde clicar**: Mostrar página do GitHub (https://github.com/LeonardoRFragoso/Legal-AI-Copilot).

**Mensagem principal**: "Sistema estabilizado, testado e pronto para apresentação."

**Risco de erro**: Nenhum.

**Plano alternativo**: N/A.
