# Roteiro de Navegação — Legal AI Copilot

> Documento principal. Cena por cena, com todas as ações, URLs, botões e resultados esperados.

---

## Cena 01 — Abertura (Webcam)

| Campo | Valor |
|-------|-------|
| **Número** | 01 |
| **Nome** | Abertura |
| **Objetivo** | Apresentar o projeto |
| **URL** | N/A (webcam ou slide) |
| **Página** | Apresentador |
| **Botões a clicar** | Nenhum |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 30s |
| **Transição** | Fade para tela do navegador |
| **Resultado esperado** | Apresentador visível, falando o nome do projeto |
| **Captura esperada** | Webcam ou slide com título "Legal AI Copilot" |
| **Checklist** | [ ] Webcam ligada, [ ] Iluminação ok, [ ] Áudio testado |
| **Observações** | Manter contato visual, não ler roteiro |
| **Plano B** | Gravar apenas áudio com slide estático |

---

## Cena 02 — Problema e Contexto (Webcam)

| Campo | Valor |
|-------|-------|
| **Número** | 02 |
| **Nome** | Problema |
| **Objetivo** | Explicar o problema |
| **URL** | N/A |
| **Página** | Apresentador |
| **Botões a clicar** | Nenhum |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 45s |
| **Transição** | Fade para diagrama de arquitetura ou webcam |
| **Resultado esperado** | Problema explicado claramente |
| **Captura esperada** | Apresentador ou slide com bullet points |
| **Checklist** | [ ] Roteiro memorizado, [ ] Tom natural |
| **Observações** | Não usar linguagem de marketing |
| **Plano B** | Slide com texto se webcam falhar |

---

## Cena 03 — Arquitetura (Webcam/Slide)

| Campo | Valor |
|-------|-------|
| **Número** | 03 |
| **Nome** | Arquitetura |
| **Objetivo** | Apresentar stack e arquitetura |
| **URL** | N/A |
| **Página** | Apresentador ou diagrama |
| **Botões a clicar** | Nenhum |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 45s |
| **Transição** | Fade para navegador na tela de login |
| **Resultado esperado** | Stack mencionada: FastAPI, React, SQLAlchemy, JWT, Agent Router |
| **Captura esperada** | Webcam ou diagrama |
| **Checklist** | [ ] Diagrama pronto se usar |
| **Observações** | Mencionar modo heurístico sem API key |
| **Plano B** | Texto na tela com bullet points da stack |

---

## Cena 04 — Login

| Campo | Valor |
|-------|-------|
| **Número** | 04 |
| **Nome** | Login |
| **Objetivo** | Demonstrar autenticação JWT com RBAC |
| **URL** | `http://localhost:5173/login` |
| **Página** | Login |
| **Botões a clicar** | 1. Botão "Advogado" (credenciais demo). 2. Botão "Entrar" |
| **Campos a preencher** | Email e senha (preenchidos automaticamente ao clicar credencial demo) |
| **Tempo estimado** | 30s |
| **Transição** | Aguardar redirect automático para `/dashboard` |
| **Resultado esperado** | Tela de login com logo da balança (Scale icon), título "Legal AI Copilot", formulário com email/senha, seção "Credenciais de demonstração" com dois botões. Após clicar "Entrar": redirect para dashboard |
| **Captura esperada** | Tela azul com gradiente (blue-50 to indigo-100), card central, ícone de balança azul |
| **Checklist** | [ ] Backend rodando, [ ] Seed executado, [ ] Credenciais demo visíveis (VITE_DEMO_MODE=true) |
| **Observações** | Mostrar que há dois perfis: Advogado e Admin. Mencionar 5 papéis RBAC |
| **Plano B** | Digitar email/senha manualmente se botão demo não funcionar |

---

## Cena 05 — Dashboard

| Campo | Valor |
|-------|-------|
| **Número** | 05 |
| **Nome** | Dashboard |
| **Objetivo** | Mostrar lista de documentos e navegação |
| **URL** | `http://localhost:5173/dashboard` |
| **Página** | Dashboard |
| **Botões a clicar** | Nenhum (apenas navegação visual). Opcional: clicar em "Upload PDF" |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 30s |
| **Transição** | Clicar em "Upload PDF" no canto superior direito |
| **Resultado esperado** | Barra de navegação superior com 9 itens (Dashboard, Upload, Chat, Análise, Riscos, Automações, Revisões, Métricas, Comparação). Nome do usuário e role badge no canto direito. Lista de documentos em cards com ícone FileText, status (Pronto/Processando), título, filename, página, data, e botões Chat/Análise/Delete |
| **Captura esperada** | Fundo cinza claro (gray-50), navbar branca, cards de documentos em grid 3 colunas |
| **Checklist** | [ ] Pelo menos 1 documento já uploaded, [ ] Navbar com todos os 9 itens visíveis |
| **Observações** | Apontar a barra de navegação item por item. Mencionar que usuários não-admin veem apenas seus documentos |
| **Plano B** | Se não houver documentos, mostrar estado vazio com mensagem "Nenhum documento encontrado" e botão "Upload PDF" |

---

## Cena 06 — Upload de Contrato

| Campo | Valor |
|-------|-------|
| **Número** | 06 |
| **Nome** | Upload |
| **Objetivo** | Demonstrar upload com processamento automático |
| **URL** | `http://localhost:5173/upload` |
| **Página** | Upload |
| **Botões a clicar** | 1. Área de drop zone (clicar para abrir file picker). 2. Botão "Fazer Upload" |
| **Campos a preencher** | Título: "Contrato de Prestação de Serviços — Demo". Arquivo: `Contrato_Prestacao_Servicos_Teste.pdf` |
| **Tempo estimado** | 60s |
| **Transição** | Aguardar tela de sucesso com CheckCircle verde, depois redirect automático para dashboard após 2s |
| **Resultado esperado** | Formulário com campo "Título do Documento" e área de upload com borda tracejada. Após selecionar arquivo: nome do arquivo visível. Após clicar "Fazer Upload": botão mostra "Processando...". Sucesso: tela verde com "Upload realizado com sucesso!" e "Redirecionando para o dashboard..." |
| **Captura esperada** | Formulário centralizado, card branco, botão azul "Fazer Upload" |
| **Checklist** | [ ] Arquivo PDF acessível, [ ] Backend rodando, [ ] Pasta uploads/ com permissão de escrita |
| **Observações** | Mencionar que o processamento em background cria chunks, embeddings (se API key), e dispara automação |
| **Plano B** | Se upload falhar, usar documento já existente no dashboard e pular para Cena 07 |

---

## Cena 07 — Análise (Resumo + Extração)

| Campo | Valor |
|-------|-------|
| **Número** | 07 |
| **Nome** | Análise |
| **Objetivo** | Mostrar resumo e extração estruturada |
| **URL** | `http://localhost:5173/analysis` (ou `http://localhost:5173/analysis?doc={id}`) |
| **Página** | Análise de Contrato |
| **Botões a clicar** | 1. Dropdown de seleção de documento (se necessário). 2. Botão "Iniciar Chat" (opcional, ao final) |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 90s |
| **Transição** | Rolar a página para baixo mostrando os 4 cards de extração. Ao final, clicar "Iniciar Chat" |
| **Resultado esperado** | Título "Análise de Contrato" com dropdown de documentos. Card de Resumo com texto gerado. Grid 2x2 com: Partes Envolvidas (ícone Users, borda azul), Datas Importantes (ícone Calendar, borda verde), Valores (ícone DollarSign, borda amber), Cláusulas Importantes (ícone Scale, borda roxa). Cada cláusula tem badge de risco (Baixo/Médio/Alto) |
| **Captura esperada** | Loading spinner durante análise. Depois: cards coloridos com informações extraídas |
| **Checklist** | [ ] Documento processado (status "ready"), [ ] Backend acessível |
| **Observações** | Mencionar que cada análise é persistida como AnalysisRecord para revisão. Rolar lentamente |
| **Plano B** | Se extração retornar vazia, tentar outro documento ou explicar que modo heurístico pode ter limitações |

---

## Cena 08 — Chat com Agent Router

| Campo | Valor |
|-------|-------|
| **Número** | 08 |
| **Nome** | Chat |
| **Objetivo** | Demonstrar chat com roteamento de intenção e guardrails |
| **URL** | `http://localhost:5173/chat` (ou `http://localhost:5173/chat?conv={id}` vindo da Análise) |
| **Página** | Chat |
| **Botões a clicar** | 1. Botão "Nova Conversa" (opcional). 2. Campo de texto. 3. Botão Send (ícone de seta) |
| **Campos a preencher** | Digitar: "Quais são os riscos deste contrato?" |
| **Tempo estimado** | 90s |
| **Transição** | Aguardar resposta do assistente, mostrar citações e disclaimer |
| **Resultado esperado** | Sidebar esquerda com lista de conversas e botão "Nova Conversa". Área principal de mensagens: mensagens do usuário em azul (direita), respostas do assistente em cinza (esquerda). Resposta comStructuredMessage se for análise de riscos: RiskBadge, título, descrição, recomendação. Disclaimer em itálico cinza claro. Campo de texto na parte inferior com placeholder "Digite sua pergunta sobre o contrato..." |
| **Captura esperada** | Interface dividida: sidebar 256px + área de chat. Mensagens com balões coloridos |
| **Checklist** | [ ] Conversa criada, [ ] Documento associado à conversa |
| **Observações** | Mostrar que o agent router classifica intenção. Mencionar guardrails: validação de confiança, citações, disclaimer. Pausar 3s após resposta para leitura |
| **Plano B** | Se resposta demorar, aguardar. Se erro, tentar pergunta mais simples como "Resuma este contrato" |

---

## Cena 09 — Análise de Riscos

| Campo | Valor |
|-------|-------|
| **Número** | 09 |
| **Nome** | Riscos |
| **Objetivo** | Demonstrar análise heurística de riscos |
| **URL** | `http://localhost:5173/risks` (ou `http://localhost:5173/risks?doc={id}`) |
| **Página** | Análise de Riscos |
| **Botões a clicar** | 1. Dropdown de documento (se necessário). 2. Botão "Analyze Risks" (azul, ícone AlertTriangle). 3. Botão "Sources" expansível em cada risk card |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 90s |
| **Transição** | Clicar "Analyze Risks", aguardar loading, mostrar resultados. Expandir "Sources" em um risk card |
| **Resultado esperado** | Card inicial com título "Análise de Riscos Contratuais" e botão "Analyze Risks". Após análise: card de Overall Risk com cor de fundo conforme severidade (verde/amarelo/laranja/vermelho), confidence score e level. Lista de RiskCards com: badge de severidade (LOW/MEDIUM/HIGH/CRITICAL), categoria, título, descrição, recomendação em box azul, confidence score. Sources expansíveis com excerpt e similarity. Card de disclaimer ao final |
| **Captura esperada** | Cards coloridos conforme severidade. Overall risk em destaque com número grande |
| **Checklist** | [ ] Documento processado, [ ] Backend rodando |
| **Observações** | Mencionar que é heurística (palavras-chave), não LLM. Similarity score é fixo (0.7) |
| **Plano B** | Se nenhum risco detectado, mostrar card verde "Nenhum risco significativo detectado" e explicar |

---

## Cena 10 — Automações

| Campo | Valor |
|-------|-------|
| **Número** | 10 |
| **Nome** | Automações |
| **Objetivo** | Mostrar pipeline de automação pós-upload |
| **URL** | `http://localhost:5173/automations` |
| **Página** | Automações |
| **Botões a clicar** | 1. Dropdown de filtro de status (opcional). 2. Botão "Atualizar" (ícone RefreshCw). 3. Botão "Tentar Novamente" em runs com falha (se houver) |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 45s |
| **Transição** | Navegar para "Revisões" na navbar |
| **Resultado esperado** | Título "Automações" com filtro de status e botão Atualizar. Lista de runs em cards: status badge (PENDING/RUNNING/COMPLETED/FAILED/PARTIAL_SUCCESS), step atual (Processando/Resumo/Riscos/Webhook/Concluído), barra de progresso com %, data, links "Ver documento" e "Ver riscos", webhook status (sent/failed/pending), tipo. Botão "Tentar Novamente" para runs FAILED/PARTIAL_SUCCESS |
| **Captura esperada** | Cards de automação com barras de progresso coloridas (verde/vermelho/amarelo/azul) |
| **Checklist** | [ ] Pelo menos 1 automação executada (após upload) |
| **Observações** | Mencionar webhook para n8n. Se webhook desabilitado, status será "pending" |
| **Plano B** | Se sem automações, mostrar estado vazio. Explicar que automação é criada no upload |

---

## Cena 11 — Revisão Humana

| Campo | Valor |
|-------|-------|
| **Número** | 11 |
| **Nome** | Revisões |
| **Objetivo** | Demonstrar workflow de revisão humana |
| **URL** | `http://localhost:5173/reviews` |
| **Página** | Revisão de Análises |
| **Botões a clicar** | 1. Filtro de tipo (opcional). 2. Filtro de status (opcional). 3. Clicar em um card de análise na lista. 4. Botão "Aprovar" ou "Rejeitar" ou "Correções". 5. Campo de comentário. 6. Botão "Confirmar Revisão" |
| **Campos a preencher** | Comentário (obrigatório para rejeição/correções, opcional para aprovação) |
| **Tempo estimado** | 60s |
| **Transição** | Após confirmar revisão, mostrar histórico atualizado. Navegar para "Métricas" |
| **Resultado esperado** | Título "Revisão de Análises" com filtros. Layout 3 colunas: lista à esquerda (cards com status badge, tipo, confiança, risco, versão, data), detalhe à direita. Detalhe mostra: tipo, status, blocked badge, metadata (confiança, nível, risco, modelo, tempo poupado, data), resumo do conteúdo, riscos estruturados, disclaimer, histórico de revisões, formulário com 3 botões (Aprovar/Rejeitar/Correções) |
| **Captura esperada** | Lista de cards à esquerda, painel de detalhe à direita com formulário de revisão |
| **Checklist** | [ ] Pelo menos 1 AnalysisRecord existente, [ ] Logado como LAWYER ou ADMIN (canReview) |
| **Observações** | Mostrar state machine: GENERATED → PENDING_REVIEW → APPROVED/REJECTED/NEEDS_CHANGES. Histórico é append-only |
| **Plano B** | Se sem análises, executar upload + chat primeiro para gerar records. Se logado como non-reviewer, mostrar mensagem "Seu perfil não permite revisar análises" |

---

## Cena 12 — Métricas de Impacto

| Campo | Valor |
|-------|-------|
| **Número** | 12 |
| **Nome** | Métricas |
| **Objetivo** | Apresentar dashboard de produtividade |
| **URL** | `http://localhost:5173/insights` |
| **Página** | Métricas de Impacto |
| **Botões a clicar** | 1. Botão "Atualizar" (ícone RefreshCw, opcional) |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 45s |
| **Transição** | Navegar para "Comparação" na navbar |
| **Resultado esperado** | 4 cards superiores: Documentos (FileText), Análises Geradas (BarChart3), Tempo Poupado em horas (TrendingUp), Taxa de Aprovação % (CheckCircle). Grid 2x2: Análises por Tipo (barras horizontais), Status das Revisões (lista), Riscos por Severidade (badges coloridos), Automações por Status (lista). Card inferior: Estimativa de Produtividade com 3 colunas (tempo manual, tempo poupado, confiança média) e aviso em itálico |
| **Captura esperada** | Dashboard com números grandes, barras de progresso, badges coloridos |
| **Checklist** | [ ] Dados de demonstração gerados (uploads, análises, revisões) |
| **Observações** | Mencionar que estimativas são do MVP, não calibradas. Ler o estimation_notice |
| **Plano B** | Se sem dados, mostrar zeros. Explicar que métricas se populam com uso |

---

## Cena 13 — Comparação de Contratos

| Campo | Valor |
|-------|-------|
| **Número** | 13 |
| **Nome** | Comparação |
| **Objetivo** | Demonstrar comparação entre dois documentos |
| **URL** | `http://localhost:5173/comparison` |
| **Página** | Comparação de Contratos |
| **Botões a clicar** | 1. Dropdown "Documento A". 2. Dropdown "Documento B". 3. Botão "Comparar Documentos" |
| **Campos a preencher** | Selecionar dois documentos diferentes |
| **Tempo estimado** | 30s |
| **Transição** | Aguardar resultado. Navegar para encerramento |
| **Resultado esperado** | Título "Comparação de Contratos". Card com 3 colunas: Documento A (dropdown), seta (ArrowRight), Documento B (dropdown). Botão "Comparar Documentos". Após comparar: card com "Resultado da Comparação" e texto com formatação markdown (bold) |
| **Captura esperada** | Layout de seleção lado a lado, resultado em texto formatado |
| **Checklist** | [ ] Pelo menos 2 documentos no sistema |
| **Observações** | Requer 2 documentos. Se houver apenas 1, mencionar limitação |
| **Plano B** | Se apenas 1 documento, fazer upload rápido de um segundo. Se comparação falhar, explicar que modo heurístico tem limitações |

---

## Cena 14 — Encerramento (Webcam)

| Campo | Valor |
|-------|-------|
| **Número** | 14 |
| **Nome** | Encerramento |
| **Objetivo** | Encerrar com limitações e próximos passos |
| **URL** | N/A (webcam ou dashboard estático) |
| **Página** | Apresentador |
| **Botões a clicar** | Nenhum |
| **Campos a preencher** | Nenhum |
| **Tempo estimado** | 60s |
| **Transição** | Fade out |
| **Resultado esperado** | Limitações listadas: heurística sem LLM, similarity fixo, sem OCR, SQLite, métricas estimadas. Próximos passos: integração com LLM, PostgreSQL, OCR |
| **Captura esperada** | Apresentador ou tela estática |
| **Checklist** | [ ] Limitações memorizadas, [ ] Tom honesto e técnico |
| **Observações** | Ser transparente sobre limitações. Não inflar capacidades |
| **Plano B** | Slide com texto das limitações |

---

## Ordem de Navegação (Resumo)

```
Login → Dashboard → Upload → Dashboard (auto) → Analysis → Chat (via "Iniciar Chat")
→ Risks → Automations → Reviews → Insights → Comparison → Encerramento
```

## URLs Validadas

| Rota | Existe | Auth |
|------|--------|------|
| `/login` | Sim | Pública |
| `/dashboard` | Sim | Protegida |
| `/upload` | Sim | Protegida |
| `/chat` | Sim | Protegida |
| `/analysis` | Sim | Protegida |
| `/risks` | Sim | Protegida |
| `/automations` | Sim | Protegida |
| `/reviews` | Sim | Protegida |
| `/insights` | Sim | Protegida |
| `/comparison` | Sim | Protegida |
