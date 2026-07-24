# Timeline da Demonstração — Legal AI Copilot

> Cronograma minuto a minuto do vídeo de apresentação. Duração total estimada: **12–15 minutos**.

---

## Visão Geral

| Bloco | Tempo | Duração | Cena |
|-------|-------|---------|------|
| 01 | 00:00–00:30 | 30s | Abertura e apresentação |
| 02 | 00:30–01:15 | 45s | Problema e contexto |
| 03 | 01:15–02:00 | 45s | Arquitetura e stack |
| 04 | 02:00–02:30 | 30s | Login |
| 05 | 02:30–03:00 | 30s | Dashboard |
| 06 | 03:00–04:00 | 60s | Upload de contrato |
| 07 | 04:00–05:30 | 90s | Análise (resumo + extração) |
| 08 | 05:30–07:00 | 90s | Chat com agent router |
| 09 | 07:00–08:30 | 90s | Análise de riscos |
| 10 | 08:30–09:15 | 45s | Automações |
| 11 | 09:15–10:15 | 60s | Revisão humana |
| 12 | 10:15–11:00 | 45s | Métricas de impacto |
| 13 | 11:00–11:30 | 30s | Comparação de contratos |
| 14 | 11:30–12:30 | 60s | Encerramento e limitações |

**Tempo total**: ~12:30 (com margem para 15:00 considerando pausas naturais)

---

## Detalhamento por Bloco

---

### Bloco 01 — Abertura e Apresentação

| Campo | Valor |
|-------|-------|
| **Tempo** | 00:00–00:30 |
| **Objetivo** | Apresentar o projeto e o apresentador |
| **Tela** | Apresentador (webcam) ou slide de título |
| **Ação** | Olhar para a câmera, apresentar-se e nomear o projeto |
| **Mensagem principal** | "Legal AI Copilot — um MVP de IA para análise de contratos jurídicos com guardrails, revisão humana e métricas de impacto" |
| **Tempo máximo** | 35s |

---

### Bloco 02 — Problema e Contexto

| Campo | Valor |
|-------|-------|
| **Tempo** | 00:30–01:15 |
| **Objetivo** | Explicar o problema que o projeto resolve |
| **Tela** | Apresentador ou slide com bullet points |
| **Ação** | Descrever o problema: análise manual de contratos é lenta, sujeita a erros e sem rastreabilidade |
| **Mensagem principal** | "Advogados gastam horas revisando contratos manualmente. O Legal AI Copilot automatiza resumo, extração, análise de riscos e Q&A — com guardrails e revisão humana" |
| **Tempo máximo** | 50s |

---

### Bloco 03 — Arquitetura e Stack

| Campo | Valor |
|-------|-------|
| **Tempo** | 01:15–02:00 |
| **Objetivo** | Apresentar a stack técnica e a arquitetura |
| **Tela** | Apresentador ou diagrama de arquitetura |
| **Ação** | Mencionar: FastAPI, React, SQLAlchemy, SQLite, JWT, RBAC, Agent Router determinístico, guardrails, heurística de riscos |
| **Mensagem principal** | "Backend em FastAPI com Python, frontend em React com TypeScript, agent router determinístico para classificação de intenção, e guardrails com validação de confiança e citações" |
| **Tempo máximo** | 50s |

---

### Bloco 04 — Login

| Campo | Valor |
|-------|-------|
| **Tempo** | 02:00–02:30 |
| **Objetivo** | Demonstrar autenticação JWT com RBAC |
| **Tela** | `http://localhost:5173/login` |
| **Ação** | Clicar em credenciais demo "Advogado", clicar "Entrar" |
| **Mensagem principal** | "Autenticação JWT com RBAC. Dois perfis demo: advogado e admin. O sistema suporta cinco papéis: admin, lawyer, assistant, client e viewer" |
| **Tempo máximo** | 35s |

---

### Bloco 05 — Dashboard

| Campo | Valor |
|-------|-------|
| **Tempo** | 02:30–03:00 |
| **Objetivo** | Mostrar a lista de documentos e navegação principal |
| **Tela** | `http://localhost:5173/dashboard` |
| **Ação** | Apontar a barra de navegação (9 itens), mostrar cards de documentos com status, botões de Chat, Análise e Delete |
| **Mensagem principal** | "O dashboard lista todos os documentos do usuário. Cada documento pode ser analisado, discutido via chat ou excluído. A barra de navegação dá acesso a todas as funcionalidades" |
| **Tempo máximo** | 35s |

---

### Bloco 06 — Upload de Contrato

| Campo | Valor |
|-------|-------|
| **Tempo** | 03:00–04:00 |
| **Objetivo** | Demonstrar o pipeline de upload com processamento automático |
| **Tela** | `http://localhost:5173/upload` |
| **Ação** | Preencher título, selecionar PDF, clicar "Fazer Upload", aguardar processamento, ver redirecionamento para dashboard |
| **Mensagem principal** | "O upload extrai texto do PDF, divide em chunks, gera embeddings se a API key estiver configurada, e dispara uma automação em background que gera resumo, análise de riscos e envia webhook" |
| **Tempo máximo** | 70s |

---

### Bloco 07 — Análise (Resumo + Extração)

| Campo | Valor |
|-------|-------|
| **Tempo** | 04:00–05:30 |
| **Objetivo** | Mostrar resumo automático e extração estruturada de informações |
| **Tela** | `http://localhost:5173/analysis` |
| **Ação** | Selecionar documento no dropdown, aguardar carregamento, mostrar resumo, rolar para ver partes, datas, valores e cláusulas com badges de risco |
| **Mensagem principal** | "A análise gera um resumo do contrato e extrai estruturadamente: partes envolvidas, datas importantes, valores monetários e cláusulas críticas — cada cláusula com classificação de risco baixo, médio ou alto" |
| **Tempo máximo** | 100s |

---

### Bloco 08 — Chat com Agent Router

| Campo | Valor |
|-------|-------|
| **Tempo** | 05:30–07:00 |
| **Objetivo** | Demonstrar o chat com roteamento determinístico de intenção e guardrails |
| **Tela** | `http://localhost:5173/chat` |
| **Ação** | Clicar em "Nova Conversa" ou selecionar conversa existente, digitar pergunta sobre o contrato, enviar, aguardar resposta com citações e disclaimer |
| **Mensagem principal** | "O chat usa um agent router determinístico que classifica a intenção do usuário — resumir, extrair, comparar, identificar riscos ou responder perguntas — e executa a ferramenta apropriada com guardrails: validação de confiança, citações obrigatórias e disclaimer jurídico" |
| **Tempo máximo** | 100s |

---

### Bloco 09 — Análise de Riscos

| Campo | Valor |
|-------|-------|
| **Tempo** | 07:00–08:30 |
| **Objetivo** | Demonstrar a análise heurística de riscos contratuais |
| **Tela** | `http://localhost:5173/risks` |
| **Ação** | Selecionar documento, clicar "Analyze Risks", aguardar resultado, mostrar overall risk, confidence score, cards de riscos com severidade, categoria, recomendação e citações expansíveis |
| **Mensagem principal** | "A análise de riscos identifica cláusulas problemáticas usando heurísticas determinísticas — confidencialidade, LGPD, rescisão, multas, pagamento, responsabilidade. Cada risco tem severidade, categoria, recomendação e citações do documento original" |
| **Tempo máximo** | 100s |

---

### Bloco 10 — Automações

| Campo | Valor |
|-------|-------|
| **Tempo** | 08:30–09:15 |
| **Objetivo** | Mostrar o pipeline de automação pós-upload com webhook |
| **Tela** | `http://localhost:5173/automations` |
| **Ação** | Mostrar lista de runs com status (PENDING, RUNNING, COMPLETED, FAILED, PARTIAL_SUCCESS), barra de progresso, step atual, webhook status, links para documento e riscos |
| **Mensagem principal** | "Cada upload dispara uma automação em background: processamento do documento, geração de resumo, análise de riscos e envio de webhook para integração com n8n. Runs com falha podem ser retentados" |
| **Tempo máximo** | 50s |

---

### Bloco 11 — Revisão Humana

| Campo | Valor |
|-------|-------|
| **Tempo** | 09:15–10:15 |
| **Objetivo** | Demonstrar o workflow de revisão humana com state machine |
| **Tela** | `http://localhost:5173/reviews` |
| **Ação** | Mostrar lista de análises com filtros por tipo e status, clicar em uma análise para ver detalhes, mostrar histórico de revisões, clicar "Aprovar" ou "Rejeitar" com comentário |
| **Mensagem principal** | "Toda análise gerada pela IA passa por revisão humana. A state machine controla o fluxo: gerada, pendente, aprovada, rejeitada ou correções necessárias. O histórico é append-only para auditoria completa" |
| **Tempo máximo** | 65s |

---

### Bloco 12 — Métricas de Impacto

| Campo | Valor |
|-------|-------|
| **Tempo** | 10:15–11:00 |
| **Objetivo** | Apresentar o dashboard de métricas e estimativas de produtividade |
| **Tela** | `http://localhost:5173/insights` |
| **Ação** | Mostrar cards de documentos, análises, tempo poupado e taxa de aprovação. Mostrar gráficos de análises por tipo, status de revisões, riscos por severidade, automações por status. Mostrar estimativa de produtividade |
| **Mensagem principal** | "O dashboard de métricas agrega documentos, análises, taxa de aprovação, riscos por severidade e estimativas de tempo economizado. As métricas de produtividade são estimativas do MVP, não calibradas com dados reais" |
| **Tempo máximo** | 50s |

---

### Bloco 13 — Comparação de Contratos

| Campo | Valor |
|-------|-------|
| **Tempo** | 11:00–11:30 |
| **Objetivo** | Demonstrar a comparação entre dois documentos |
| **Tela** | `http://localhost:5173/comparison` |
| **Ação** | Selecionar Documento A e Documento B nos dropdowns, clicar "Comparar Documentos", aguardar resultado |
| **Mensagem principal** | "A comparação analisa dois contratos lado a lado, identificando semelhanças e diferenças. Requer pelo menos dois documentos no sistema" |
| **Tempo máximo** | 35s |

---

### Bloco 14 — Encerramento e Limitações

| Campo | Valor |
|-------|-------|
| **Tempo** | 11:30–12:30 |
| **Objetivo** | Encerrar a apresentação mencionando limitações honestas e próximos passos |
| **Tela** | Apresentador (webcam) ou tela estática do dashboard |
| **Ação** | Listar limitações: análise heurística sem LLM, similarity score fixo, sem OCR, SQLite, métricas estimadas. Mencionar que o sistema funciona em modo heurístico sem OpenAI API key |
| **Mensagem principal** | "O Legal AI Copilot é um MVP funcional com limitações transparentes: a análise de riscos é heurística, não usa LLM; o similarity score é fixo; não há OCR; usa SQLite; e as métricas são estimativas. O sistema opera em modo heurístico sem necessidade de API key" |
| **Tempo máximo** | 70s |
