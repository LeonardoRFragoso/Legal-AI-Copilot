# Case Final — Respostas às Perguntas

## 1. Qual LLM foi escolhido e por quê?

**Versão curta**: OpenAI GPT-4o, via LangChain. Escolhido pela qualidade em português, capacidade de seguir prompts estruturados (JSON), e ecossistema maduro de integração com LangChain.

**Versão detalhada**: O projeto utiliza GPT-4o como LLM para as operações de resumo, extração, comparação e Q&A. A escolha se baseou em três fatores: (1) qualidade superior em português brasileiro, essencial para contratos jurídicos; (2) capacidade de retornar JSON estruturado confiável quando instruído via prompt, usado na extração de informações; (3) integração nativa com LangChain, que simplifica a construção do agente com tools. A temperatura é 0.3 para reduzir criatividade e manter respostas factuais.

**Exemplo prático**: A ferramenta `extract_information` envia um prompt que pede explicitamente "return ONLY a valid JSON object" com campos parties, dates, values e clauses. O GPT-4o retorna o JSON que é parseado e validado.

---

## 2. Como foi utilizada Engenharia de Prompts?

**Versão curta**: Prompts estruturados em português (pt-BR) com instruções explícitas de formato, schema JSON para extração, e prompts comparativos com estrutura definida. Temperatura baixa (0.3) para reduzir alucinação.

**Versão detalhada**: A engenharia de prompts foi aplicada em três ferramentas principais. No resumo, o prompt instrui "Faça um resumo detalhado do seguinte documento legal em português (pt-BR)". Na extração, o prompt define um schema JSON explícito com os campos esperados e exige "return ONLY a valid JSON object with no additional text", com fallback de parsing que remove markdown code blocks. Na comparação, o prompt estrutura a resposta em seções (diferenças, cláusulas únicas, recomendações). Em Q&A, o LangChain Agent Executor gerencia o prompt com histórico de conversa e contexto recuperado via RAG.

**Exemplo prático**: O prompt de extração inclui o schema completo: `{"parties": [...], "dates": [...], "values": [...], "clauses": [...]}`. Se o LLM retornar JSON com markdown, o código remove os delimitadores ```json antes do parse.

---

## 3. Como o agente decide quais ações executar?

**Versão curta**: O Agent Router é determinístico, baseado em palavras-chave. Sem LLM na decisão. Mapeia a mensagem do usuário para uma de 5 intents (SUMMARIZE, EXTRACT, COMPARE, IDENTIFY_RISKS, QUESTION_ANSWERING) ou UNKNOWN.

**Versão detalhada**: O `LegalAgentRouter` em `agent_router.py` classifica a intenção usando um conjunto de palavras-chave pré-definidas em português e inglês. Por exemplo, "resumo" e "resumir" mapeiam para SUMMARIZE_DOCUMENT; "riscos" e "risk" mapeiam para IDENTIFY_RISKS. A primeira correspondência vence. O router retorna um `RouterDecision` com intent, tool, reason (curto e seguro, sem chain-of-thought) e confidence. A vantagem da abordagem determinística é previsibilidade, velocidade e custo zero — não consome tokens do LLM para roteamento.

**Exemplo prático**: Usuário digita "identifique os riscos do contrato" → Router detecta "riscos" → IDENTIFY_RISKS → executa `contract_risk_analysis` (heurístico, sem LLM). Se digitasse "qual o valor do contrato" → detecta "qual" → QUESTION_ANSWERING → executa `semantic_search` (GPT-4o + RAG).

---

## 4. Como o RAG foi estruturado para documentos jurídicos?

**Versão curta**: Upload de PDF → extração de texto → chunking por sentenças (1000 chars, 200 overlap) → embeddings via OpenAI text-embedding-3-small → armazenamento binário no SQLite → busca por similaridade cosseno na query do usuário.

**Versão detalhada**: O pipeline de RAG começa com a extração de texto do PDF via PyPDF2. O texto é dividido em chunks pelo `chunker.py` usando divisão por sentenças com tamanho máximo de 1000 caracteres e sobreposição de 200. Cada chunk recebe um embedding gerado pela OpenAI API (modelo text-embedding-3-small), que é serializado com pickle e armazenado na tabela `document_embeddings`. Na busca, o embedding da pergunta do usuário é comparado com todos os embeddings do documento via similaridade cosseno (numpy), e os top-K chunks são recuperados como contexto para o GPT-4o. O RAG é usado **apenas** na ferramenta `semantic_search` (Q&A). As outras ferramentas (resumo, extração, comparação) enviam o texto completo dos chunks ao LLM sem recuperação semântica.

**Exemplo prático**: Usuário pergunta "qual é a cláusula de rescisão?" → embedding da query é gerado → comparado com embeddings de todos os chunks → chunks com maior similaridade cosseno são selecionados → enviados como contexto ao GPT-4o → resposta com citações.

---

## 5. Como a solução evita alucinações?

**Versão curta**: O AIValidator aplica validação determinística pós-LLM em Q&A: calcula confidence score (0-100) baseado em fontes, similaridade, citações e consistência. Score < 60 bloqueia a resposta. Disclaimer jurídico é sempre exibido.

**Versão detalhada**: O controle de alucinação opera em três camadas. Primeiro, o RAG garante que o LLM receba apenas contexto dos documentos reais, não conhecimento genérico. Segundo, o `AIValidator` em `ai_validator.py` valida a resposta após a geração: verifica se existem chunks recuperados, se há citações, se a similaridade média é adequada, e calcula um score de 0-100. Se o score for inferior a 60, a resposta é bloqueada e o conteúdo não é exibido ao usuário — apenas uma mensagem padrão de "evidências insuficientes". Terceiro, o disclaimer jurídico é sempre presente, mesmo em respostas bloqueadas. Importante: o AIValidator é aplicado **apenas em Q&A** (`semantic_search`). Resumo, extração e comparação usam LLM diretamente sem validação posterior. A análise de riscos é heurística e não gera texto livre, então não está sujeita a alucinação de LLM.

**Exemplo prático**: Usuário pergunta sobre "taxa de juros" em um contrato que não menciona juros → 0 chunks recuperados → confidence score = 0 → resposta bloqueada → usuário vê "Não encontrei evidências suficientes nos documentos selecionados para responder com segurança."

---

## 6. Como falhas e erros são monitorados?

**Versão curta**: Logging estruturado em JSON via `logger.py` em todos os componentes. Eventos de início, conclusão e falha de cada tool. Erros de webhook, automação e validação registrados. Sem observabilidade externa (Grafana/Prometheus).

**Versão detalhada**: O sistema usa um logger customizado (`app/logger.py`) que registra eventos em formato JSON estruturado com timestamp, level, message e metadados. Cada execução de tool registra `agent_tool_started` e `agent_tool_completed` (ou `agent_tool_failed`) com duration_ms, tool name, document_id e error_type. O webhook service registra tentativas, timeouts e falhas. O automation service registra mudanças de status e step. Dados sensíveis (tokens JWT, senhas, conteúdo integral de documentos) não são logados. Não há integração com Grafana, Prometheus ou sistemas de APM. O endpoint `/admin/system-status` fornece uma visão agregada para administradores (runs por status, webhooks falhados, duração média).

**Exemplo prático**: Quando o webhook falha por timeout, o log registra `{"event": "webhook_failed", "error_type": "TimeoutException", "retry_count": 2}` e o AutomationRun é marcado como PARTIAL_SUCCESS com webhook_status="failed".

---

## 7. Quais cuidados adicionais seriam necessários em segurança, confiabilidade e privacidade?

**Versão curta**: Migrar para PostgreSQL com criptografia em repouso, usar Celery + Redis para fila de tarefas, implementar rate limiting, auditoria de acesso, LGPD compliance (anonimização, retenção), refresh token com rotação, e testes de penetração.

**Versão detalhada**: Em segurança, seria necessário adicionar rate limiting por usuário/IP, auditoria de acesso (quem acessou qual documento e quando), rotação de refresh tokens, e validação de entrada mais rigorosa (tamanho máximo de PDF, sanitização de nomes de arquivo). Em confiabilidade, a migração para Celery + Redis eliminaria o risco de perda de BackgroundTasks em restart, e PostgreSQL com backups automáticos substituiria o SQLite. Em privacidade, considerando que contratos jurídicos contêm dados sensíveis, seria necessário criptografia em repouso no banco, política de retenção e expiração de documentos, anonimização em logs, conformidade explícita com LGPD (base legal, consentimento, direitos do titular), e idealmente execução em infraestrutura dedicada ou VPC isolada. A análise de riscos do próprio sistema identifica a ausência de cláusulas de LGPD nos contratos analisados — irônico que o sistema precisa da mesma conformidade.

**Exemplo prático**: Hoje, se o servidor reinicia durante uma automação, o BackgroundTask é perdido e o AutomationRun fica em status RUNNING indefinidamente. Com Celery, a tarefa seria re-enfileirada automaticamente.
