# Interview Quick Reference — Respostas de 20 a 40 Segundos

## Por que FastAPI?

FastAPI oferece tipagem nativa com Pydantic, documentação OpenAPI automática, performance assíncrona nativa, e integração simples com BackgroundTasks. Para um MVP que precisa de API REST rápida com validação de schema, é a escolha ideal — menos boilerplate que Flask, mais simples que Django para este escopo.

## Por que SQLite no MVP?

SQLite dispensa configuração de servidor, reduz fricção de setup, e é suficiente para demonstrar o fluxo completo. O SQLAlchemy abstrai o acesso, então a migração para PostgreSQL é apenas trocar a connection string. A limitação real é concorrência de escrita, que não é problema para demo.

## Por que Agent Router determinístico?

Porque roteamento por palavras-chave é instantâneo, gratuito e reproduzível. Não consome tokens do LLM para decidir qual tool executar. Um router baseado em LLM adicionaria latência, custo e imprevisibilidade — para 5 intents bem definidas, heurística é suficiente e mais confiável.

## Por que revisão humana?

Porque IA jurídica sem supervisão humana é irresponsável. O sistema persiste toda análise como AnalysisRecord, permite aprovar, rejeitar ou pedir alterações, e mantém histórico append-only. O humano é o guardrail final — a IA acelera, mas o profissional decide.

## Por que não usar LLM no Risk Analyzer?

Porque detecção de cláusulas ausentes e padrões problemáticos é mais confiável com regras determinísticas. Palavras-chave como "multa ilimitada" ou ausência de "confidencialidade" são verificações exatas, não interpretações subjetivas. LLM poderia alucinar riscos ou perder óbvios. Heurística é reproduzível, auditável e gratuita.

## Como evitar alucinação?

O AIValidator calcula confidence score baseado em evidências reais (chunks recuperados, similaridade, citações). Score abaixo de 60 bloqueia a resposta — o usuário vê "evidências insuficientes" em vez de uma resposta fabricada. O RAG também garante que o LLM receba apenas contexto dos documentos, não conhecimento genérico.

## Como escalar?

Migrar SQLite para PostgreSQL, BackgroundTasks para Celery + Redis, adicionar load balancer com múltiplos workers FastAPI, cache de embeddings com Redis, e CDN para o frontend. A arquitetura com SQLAlchemy e camadas de serviço facilita — a maioria das mudanças é de infraestrutura, não de código.

## Como migrar para PostgreSQL?

Trocar `SQLALCHEMY_DATABASE_URL` de SQLite para PostgreSQL no `database.py`, ajustar `connect_args` (remover `check_same_thread`), e rodar `alembic upgrade head`. O SQLAlchemy abstrai a maioria das diferenças. Atenção a tipos JSON e serialização de embeddings (pickle → JSONB ou array).

## Como substituir BackgroundTasks?

Implementar Celery com Redis como broker. Criar uma task Celery que encapsula a lógica do `automation_service.py`, substituir a chamada de BackgroundTasks por `.delay()`, e adicionar um worker Celery ao docker-compose. O AutomationRun já rastreia status, então a integração é direta.

## Como proteger dados jurídicos?

Criptografia em repouso no banco, TLS em trânsito, política de retenção e expiração de documentos, anonimização em logs, conformidade explícita com LGPD (base legal, consentimento, direitos do titular), execução em VPC isolada, e auditoria de acesso (quem acessou qual documento e quando).

## Como medir ROI real?

Calibrar as estimativas manuais com tempo real de revisão antes e depois do sistema. Medir: tempo médio de revisão com e sem IA, taxa de aprovação na primeira revisão, número de riscos identificados que o humano não teria pegado, e tempo economizado por tipo de análise. As métricas atuais são estimativas configuráveis, não medidas.

## O que faria com mais tempo?

Integraria AIValidator em todas as operações com LLM (não apenas Q&A), adicionaria RAG semântico na análise de riscos, implementaria OCR para PDFs escaneados, adicionaria testes frontend com Playwright, migraria para PostgreSQL + Celery, e calibraria métricas com dados reais de escritórios.

## Maior desafio técnico?

Garantir que o sistema bloqueie alucinações sem bloquear respostas legítimas. O threshold de confidence score (60) é um trade-off — muito alto bloqueia respostas úteis, muito baixo deixa passar alucinações. Calibrar isso requer dados reais e testes extensivos, que não fiz no MVP.

## Principal trade-off?

Usar heurística no Risk Analyzer em vez de LLM. Ganha-se reprodutibilidade, custo zero e velocidade, mas perde-se a capacidade de detectar riscos sutis que exigem interpretação semântica. A decisão foi consciente — para MVP, determinismo é mais valioso que flexibilidade.

## Principal limitação?

O AIValidator está integrado apenas em Q&A. Resumo, extração e comparação usam GPT-4o diretamente sem validação posterior. Isso significa que essas operações podem produzir respostas sem evidência documental adequada, sem o bloqueio automático que existe em Q&A.
