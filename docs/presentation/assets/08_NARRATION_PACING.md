# Narration Pacing Guide — Legal AI Copilot

> Guia de sincronização entre fala (narração em off), movimento do cursor,
> tempo de leitura visual, mudança de página e scroll.
> Referência cruzada com `04_VIDEO_SPEECH_SCRIPT.md` e `11_SCREEN_RECORDING_SHOTLIST.md`.

---

## 1. Princípios de Sincronização

### Regra Fundamental

A fala guia o ritmo. O cursor segue a fala. A tela segue o cursor.

```
Fala → Cursor → Tela → Leitura → Próxima ação
```

### Hierarquia de Sincronização

| Prioridade | Elemento | Como sincronizar |
|------------|----------|-----------------|
| 1 | Fala | Narração em off gravada separadamente |
| 2 | Cursor | Move-se para o elemento mencionado na fala |
| 3 | Clique | Ocorre quando a fala indica a ação |
| 4 | Tela | Carrega após o clique — aguardar completamente |
| 5 | Leitura | Cursor para sobre o resultado — tempo de absorção |
| 6 | Próxima ação | Iniciar apenas após o tempo de leitura completar |

---

## 2. Pacing por Cena

### Cena 01 — Abertura (00:00–00:30)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 00:00 | [Silêncio 3s] | Parado no centro | Login estático |
| 00:03 | "Este é o Legal AI Copilot..." | Move-se para o logo | Login |
| 00:05 | [Fala sobre o projeto] | Parado sobre o logo | Login |
| 00:08 | [Pausa 1s] | Parado | Login |
| 00:09 | "Nesta demonstração, vou percorrer..." | Move-se para o título | Login |
| 00:12 | [Fala sobre escopo] | Parado sob o título | Login |
| 00:18 | [Fala continua] | Move-se de volta ao centro | Login |
| 00:22 | [Fala continua] | Move-se para credenciais demo | Login |
| 00:25 | [Fala final] | Parado sobre credenciais | Login |
| 00:28 | [Silêncio 2s] | Move-se ao centro | Login estático |

**Ritmo**: Lento. 3s de silêncio inicial. Pausas respiradas de 1s entre frases.

---

### Cena 02 — Problema (00:30–01:15)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 00:30 | "A análise manual de contratos..." | Parado no centro | Login |
| 00:35 | [Fala sobre o problema] | Move-se para campo email | Login |
| 00:37 | [Fala continua] | Parado sobre email | Login |
| 00:40 | [Pausa 1s] | Parado | Login |
| 00:41 | "O Legal AI Copilot aborda..." | Move-se para campo senha | Login |
| 00:43 | [Fala sobre a solução] | Parado sobre senha | Login |
| 00:46 | [Fala continua] | Move-se para botão Entrar | Login |
| 00:48 | [Fala continua] | Parado sobre Entrar | Login |
| 00:52 | [Fala final] | Move-se ao centro | Login |
| 01:00 | [Fala final] | Parado no centro | Login |
| 01:08 | [Silêncio] | Move-se a posição neutra | Login |
| 01:13 | [Silêncio 2s] | Parado | Login estático |

**Ritmo**: Moderado. Pausa de 1s entre o problema e a solução.

---

### Cena 03 — Arquitetura (01:15–02:00)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 01:15 | "A stack do projeto inclui..." | Em posição neutra | Login |
| 01:20 | [Fala sobre FastAPI, React] | Move-se para botão Advogado | Login |
| 01:23 | [Fala continua] | Parado sobre Advogado | Login |
| 01:26 | [Pausa 1s] | Parado | Login |
| 01:27 | "A autenticação usa JWT..." | Move-se para botão Admin | Login |
| 01:30 | [Fala sobre RBAC] | Parado sobre Admin | Login |
| 01:33 | [Pausa 1s] | Parado | Login |
| 01:34 | "O agent router é determinístico..." | Move-se ao centro | Login |
| 01:37 | [Fala sobre guardrails] | Parado no centro | Login |
| 01:42 | [Fala final] | Move-se para botão Entrar | Login |
| 01:45 | [Fala final] | Parado sobre Entrar | Login |
| 01:52 | [Silêncio 2s] | Parado | Login estático |

**Ritmo**: Moderado. Pausas de 1s entre tópicos técnicos (stack, auth, agent router).

---

### Cena 04 — Login (02:00–02:30)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 02:00 | "A tela de login oferece dois perfis..." | Move-se para Advogado | Login |
| 02:02 | [Fala sobre perfis] | Parado sobre Advogado | Login |
| 02:03 | [Pausa 500ms antes do clique] | Parado | Login |
| 02:04 | [Clique "Advogado"] | — | Campos preenchidos |
| 02:05 | "Vou usar o perfil de advogado..." | Parado (campos preenchidos) | Login |
| 02:07 | [Fala continua] | Move-se para Entrar | Login |
| 02:09 | [Pausa 500ms antes do clique] | Parado | Login |
| 02:10 | [Clique "Entrar"] | — | Redirect → Dashboard |
| 02:11 | "O sistema autentica com JWT..." | Parado (aguardar redirect) | Dashboard carregando |
| 02:13 | [Fala sobre redirect] | Parado | Dashboard carregado |
| 02:18 | [Fala final] | Parado no centro | Dashboard estático |
| 02:25 | [Silêncio] | Parado | Dashboard |

**Ritmo**: Dinâmico. Cliques rápidos. Aguardar redirect.

---

### Cena 05 — Dashboard (02:30–03:00)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 02:30 | "O dashboard lista todos os documentos..." | Parado no centro | Dashboard |
| 02:32 | [Fala sobre documentos] | Move-se para navbar | Dashboard |
| 02:34 | "A barra de navegação superior..." | Percorre navbar item por item | Dashboard |
| 02:39 | [Fala sobre 9 itens] | Parado em "Comparação" | Dashboard |
| 02:41 | [Fala sobre usuário] | Move-se para nome/role | Dashboard |
| 02:43 | "No canto direito, vemos o nome..." | Parado sobre nome/role | Dashboard |
| 02:45 | [Fala sobre role] | Move-se para primeiro card | Dashboard |
| 02:47 | [Fala sobre card] | Parado sobre o card | Dashboard |
| 02:49 | [Fala final] | Move-se para "Upload PDF" | Dashboard |
| 02:52 | [Pausa 500ms] | Parado sobre "Upload PDF" | Dashboard |
| 02:53 | [Clique "Upload PDF"] | — | Navegação para /upload |
| 02:55 | [Fala sobre upload] | Parado (aguardar carregamento) | Upload carregando |
| 02:58 | [Silêncio] | Parado | Upload carregado |

**Ritmo**: Moderado. Navbar percorrida em ~5s (300ms por item).

---

### Cena 06 — Upload (03:00–04:00)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 03:00 | "Vou fazer o upload de um contrato..." | Parado no centro | Upload |
| 03:02 | [Fala sobre upload] | Move-se para campo título | Upload |
| 03:03 | [Clique no campo] | — | Campo focado |
| 03:04 | [Digitação do título] | Parado no campo | Campo sendo preenchido |
| 03:08 | [Fala sobre processamento] | Move-se para drop zone | Upload |
| 03:09 | [Clique na drop zone] | — | File picker abre |
| 03:10 | [Seleção de arquivo] | Move-se no file picker | File picker |
| 03:12 | [Arquivo selecionado] | Parado | Nome do arquivo visível |
| 03:14 | [Fala sobre extração] | Move-se para "Fazer Upload" | Upload |
| 03:15 | [Pausa 500ms] | Parado | Upload |
| 03:16 | [Clique "Fazer Upload"] | — | "Processando..." |
| 03:17 | "O processamento extrai o texto..." | Parado (NÃO mover) | Loading |
| 03:20 | [Fala sobre chunks] | Parado | Loading |
| 03:25 | [Loading completa] | Parado | Tela de sucesso |
| 03:26 | "Upload concluído..." | Parado | CheckCircle verde |
| 03:29 | [Fala sobre dashboard] | Parado | Redirect → Dashboard |
| 03:31 | [Fala final] | Parado no centro | Dashboard com novo doc |
| 03:55 | [Silêncio] | Parado | Dashboard |

**Ritmo**: Moderado. Digitação natural. Loading aguardado completamente. NÃO mover cursor durante loading.

---

### Cena 07 — Análise (04:00–05:30)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 04:00 | [Clique "Análise" na navbar] | — | Navegação para /analysis |
| 04:02 | "A página de análise gera um resumo..." | Parado | Analysis carregando |
| 04:04 | [Seleção de documento no dropdown] | Move-se para dropdown | Dropdown |
| 04:06 | [Documento selecionado] | — | Loading spinner |
| 04:07 | [Fala sobre resumo] | Parado (NÃO mover) | Spinner |
| 04:12 | [Loading completa] | Parado | Resumo visível |
| 04:13 | "O resumo é gerado automaticamente..." | Move-se para card de resumo | Analysis |
| 04:15 | [Fala sobre conteúdo] | Parado sobre o resumo | Analysis |
| 04:18 | "Abaixo, temos quatro cards..." | Scroll para baixo | Grid 2x2 visível |
| 04:20 | [Fala sobre grid] | Parado | Grid 2x2 |
| 04:22 | "As partes identificadas incluem..." | Move-se para Partes | Card Partes |
| 04:25 | [Fala sobre partes] | Parado sobre Partes | Card Partes |
| 04:28 | "As datas extraídas incluem..." | Move-se para Datas | Card Datas |
| 04:31 | [Fala sobre datas] | Parado sobre Datas | Card Datas |
| 04:34 | "Os valores monetários são identificados..." | Move-se para Valores | Card Valores |
| 04:37 | [Fala sobre valores] | Parado sobre Valores | Card Valores |
| 04:40 | "Cada cláusula tem um badge de risco..." | Move-se para Cláusulas | Card Cláusulas |
| 04:43 | [Fala sobre badges] | Move-se sobre os badges | Badges visíveis |
| 04:46 | [Fala final] | Parado sobre Cláusulas | Card Cláusulas |
| 04:50 | [Fala sobre chat] | Scroll para cima + move para "Iniciar Chat" | Botão visível |
| 05:25 | [Silêncio] | Parado | Analysis |

**Ritmo**: Moderado. 3s de leitura por card. Scroll suave.

---

### Cena 08 — Chat (05:30–07:00)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 05:30 | [Clique "Iniciar Chat"] | — | Navegação para /chat |
| 05:32 | "O chat permite interagir..." | Parado no centro | Chat |
| 05:34 | [Fala sobre chat] | Move-se para sidebar | Sidebar |
| 05:36 | "A barra lateral mostra conversas..." | Parado sobre conversa | Sidebar |
| 05:38 | [Fala sobre conversas] | Move-se para campo de texto | Campo de texto |
| 05:40 | [Clique no campo] | — | Campo focado |
| 05:41 | [Digitação da pergunta] | Parado no campo | Texto sendo digitado |
| 05:44 | "O agent router classifica a intenção..." | Move-se para Send | Send visível |
| 05:45 | [Pausa 500ms] | Parado | — |
| 05:46 | [Clique Send] | — | Mensagem enviada |
| 05:47 | [Fala sobre roteamento] | Parado (NÃO mover) | Aguardando resposta |
| 05:50 | [Fala sobre guardrails] | Parado | Loading |
| 05:55 | [Resposta aparece] | Parado | Resposta visível |
| 05:58 | "A resposta inclui riscos identificados..." | Move-se para resposta | Resposta |
| 06:01 | [Fala sobre estrutura] | Parado sobre resposta | Risk cards na resposta |
| 06:04 | "Cada resposta inclui citações..." | Move-se para citações | Citações |
| 06:07 | [Fala sobre citações] | Parado sobre citações | Citações visíveis |
| 06:10 | "E um disclaimer jurídico..." | Scroll + move para disclaimer | Disclaimer |
| 06:13 | [Fala sobre disclaimer] | Parado sobre disclaimer | Disclaimer visível |
| 06:16 | [Fala final] | Move-se a posição neutra | Chat |
| 06:55 | [Silêncio] | Parado | Chat |

**Ritmo**: Moderado. Digitação natural. Resposta aguardada completamente. 3s de leitura para resposta, citações e disclaimer.

---

### Cena 09 — Riscos (07:00–08:30)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 07:00 | [Clique "Riscos" na navbar] | — | Navegação para /risks |
| 07:02 | "A página de análise de riscos..." | Parado | Risks |
| 07:04 | [Seleção de documento] | Move-se para dropdown | Dropdown |
| 07:06 | [Documento selecionado] | — | Tela de análise |
| 07:08 | [Fala sobre análise] | Move-se para "Analyze Risks" | Botão visível |
| 07:10 | [Pausa 500ms] | Parado | — |
| 07:11 | [Clique "Analyze Risks"] | — | Loading |
| 07:12 | [Fala sobre heurística] | Parado (NÃO mover) | Loading |
| 07:17 | [Loading completa] | Parado | Overall risk visível |
| 07:18 | "O resultado mostra um risco geral..." | Move-se para overall risk | Overall risk card |
| 07:21 | [Fala sobre confidence] | Parado sobre overall risk | Card visível |
| 07:24 | "Cada risco identificado tem severidade..." | Move-se para risk card | Risk card |
| 07:27 | [Fala sobre severidade] | Parado sobre risk card | Badge visível |
| 07:30 | "As citações mostram o trecho exato..." | Move-se para "Sources" | Sources botão |
| 07:32 | [Clique "Sources"] | — | Sources expandindo |
| 07:34 | [Fala sobre sources] | Move-se para conteúdo expandido | Sources visíveis |
| 07:37 | [Fala sobre excerpt] | Parado sobre sources | Excerpt + page + similarity |
| 07:40 | "É importante destacar que esta análise é heurística..." | Scroll + move para disclaimer | Disclaimer |
| 07:43 | [Fala sobre limitação] | Parado sobre disclaimer | Disclaimer visível |
| 07:46 | [Fala final] | Move-se a posição neutra | Risks |
| 08:25 | [Silêncio] | Parado | Risks |

**Ritmo**: Moderado. Loading aguardado. 3s de leitura para overall risk, risk card, sources e disclaimer.

---

### Cena 10 — Automações (08:30–09:15)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 08:30 | [Clique "Automações" na navbar] | — | Navegação para /automations |
| 08:32 | "Cada upload dispara uma automação..." | Parado no centro | Automações |
| 08:34 | [Fala sobre pipeline] | Move-se para primeiro card | Card de automação |
| 08:37 | "Cada run mostra o status..." | Move-se para status badge | Status badge |
| 08:39 | [Fala sobre status] | Parado sobre status | Badge visível |
| 08:41 | [Fala sobre progresso] | Move-se para barra de progresso | Barra visível |
| 08:43 | [Fala sobre webhook] | Move-se para webhook status | Webhook visível |
| 08:45 | "É possível filtrar por status..." | Move-se para filtro | Filtro visível |
| 08:47 | [Fala sobre filtro] | Move-se para "Atualizar" | Botão visível |
| 08:49 | "Cada run tem links diretos..." | Scroll + move para links | Links visíveis |
| 08:51 | [Fala sobre links] | Parado sobre "Ver documento" | Link visível |
| 08:53 | [Fala sobre "Ver riscos"] | Move-se para "Ver riscos" | Link visível |
| 08:55 | [Fala final] | Move-se a posição neutra | Automações |
| 09:10 | [Silêncio] | Parado | Automações |

**Ritmo**: Dinâmico. Movimentos rápidos entre elementos. 2s de leitura por elemento.

---

### Cena 11 — Revisões (09:15–10:15)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 09:15 | [Clique "Revisões" na navbar] | — | Navegação para /reviews |
| 09:17 | "A revisão humana é o controle de qualidade..." | Parado no centro | Revisões |
| 09:19 | [Fala sobre revisão] | Move-se para filtros | Filtros visíveis |
| 09:21 | [Fala sobre lista] | Move-se para primeiro card | Card na lista |
| 09:23 | "A lista mostra cada análise..." | Parado sobre o card | Status + tipo + confiança |
| 09:25 | [Clique no card] | — | Painel de detalhe abre |
| 09:27 | "O painel de detalhe mostra..." | Parado (aguardar carregamento) | Detalhe carregando |
| 09:29 | [Fala sobre detalhe] | Move-se para conteúdo | Detalhe visível |
| 09:32 | [Fala sobre conteúdo] | Parado sobre conteúdo | Content_summary visível |
| 09:35 | "O histórico é append-only..." | Scroll para histórico | Histórico visível |
| 09:37 | [Fala sobre histórico] | Move-se para histórico | Histórico visível |
| 09:40 | [Fala sobre state machine] | Move-se para botões | 3 botões visíveis |
| 09:42 | [Pausa 500ms] | Parado sobre "Aprovar" | — |
| 09:43 | [Clique "Aprovar"] | — | Formulário visível |
| 09:44 | [Fala sobre formulário] | Move-se para campo de comentário | Campo visível |
| 09:45 | [Clique no campo] | — | Campo focado |
| 09:46 | [Digitação do comentário] | Parado no campo | Texto sendo digitado |
| 09:49 | "A state machine controla o fluxo..." | Move-se para "Confirmar Revisão" | Botão visível |
| 09:50 | [Pausa 500ms] | Parado | — |
| 09:51 | [Clique "Confirmar Revisão"] | — | Revisão enviada |
| 09:52 | [Fala sobre atualização] | Parado (aguardar) | Histórico atualizando |
| 09:54 | [Fala final] | Parado | Histórico atualizado |
| 09:57 | [Silêncio] | Parado | Histórico visível |
| 10:10 | [Silêncio] | Parado | Revisões |

**Ritmo**: Moderado. 3s de leitura para detalhe e histórico. Digitação natural.

---

### Cena 12 — Métricas (10:15–11:00)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 10:15 | [Clique "Métricas" na navbar] | — | Navegação para /insights |
| 10:17 | "O dashboard de métricas agrega..." | Parado no centro | Métricas |
| 10:19 | "Os cards superiores mostram..." | Move-se para card 1 (Documentos) | Card visível |
| 10:21 | [Fala sobre documentos] | Move-se para card 2 (Análises) | Card visível |
| 10:23 | [Fala sobre análises] | Move-se para card 3 (Tempo) | Card visível |
| 10:25 | [Fala sobre tempo poupado] | Move-se para card 4 (Aprovação) | Card visível |
| 10:27 | "Abaixo, quatro visualizações..." | Scroll para grid 2x2 | Grid visível |
| 10:29 | [Fala sobre análises por tipo] | Move-se para "Análises por Tipo" | Barras visíveis |
| 10:31 | [Fala sobre status das revisões] | Move-se para "Status das Revisões" | Lista visível |
| 10:33 | [Fala sobre riscos por severidade] | Move-se para "Riscos por Severidade" | Badges visíveis |
| 10:35 | [Fala sobre automações] | Move-se para "Automações por Status" | Lista visível |
| 10:37 | "A estimativa de produtividade compara..." | Scroll para estimativa | Estimativa visível |
| 10:39 | [Fala sobre estimativa] | Move-se para estimativa | 3 colunas visíveis |
| 10:42 | "Administradores veem métricas globais..." | Move-se para aviso | Aviso visível |
| 10:45 | [Fala sobre aviso] | Parado sobre aviso | Aviso em itálico |
| 10:48 | [Fala final] | Move-se a posição neutra | Métricas |
| 10:55 | [Silêncio] | Parado | Métricas |

**Ritmo**: Dinâmico. 2s por card. Scroll suave entre seções.

---

### Cena 13 — Comparação (11:00–11:30)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 11:00 | [Clique "Comparação" na navbar] | — | Navegação para /comparison |
| 11:02 | "A comparação permite analisar..." | Parado no centro | Comparação |
| 11:04 | [Fala sobre comparação] | Move-se para dropdown A | Dropdown A |
| 11:05 | [Clique dropdown A] | — | Lista abre |
| 11:06 | [Selecionar doc A] | Move-se para opção | Opção selecionada |
| 11:07 | [Fala sobre doc A] | Move-se para dropdown B | Dropdown B |
| 11:08 | [Clique dropdown B] | — | Lista abre |
| 11:09 | [Selecionar doc B] | Move-se para opção | Opção selecionada |
| 11:10 | [Fala sobre docs selecionados] | Move-se para "Comparar" | Botão visível |
| 11:11 | [Pausa 500ms] | Parado | — |
| 11:12 | [Clique "Comparar Documentos"] | — | Loading |
| 11:13 | "O resultado destaca semelhanças..." | Parado (NÃO mover) | Loading |
| 11:18 | [Loading completa] | Parado | Resultado visível |
| 11:19 | [Fala sobre resultado] | Move-se para resultado | Resultado visível |
| 11:22 | [Fala final] | Move-se a posição neutra | Comparação |
| 11:25 | [Silêncio] | Parado | Comparação |

**Ritmo**: Rápido. Seleções rápidas. Loading aguardado. 3s de leitura do resultado.

---

### Cena 14 — Encerramento (11:30–12:30)

| Tempo | Fala | Cursor | Tela |
|-------|------|--------|------|
| 11:30 | [Clique "Dashboard" na navbar] | — | Navegação para /dashboard |
| 11:32 | "Para concluir, é importante ser transparente..." | Parado no centro | Dashboard |
| 11:37 | [Pausa 1s] | Parado | Dashboard |
| 11:38 | "A análise de riscos é heurística..." | Parado | Dashboard |
| 11:43 | [Pausa 1s] | Parado | Dashboard |
| 11:44 | "O sistema funciona em modo heurístico..." | Parado | Dashboard |
| 11:49 | [Pausa 1s] | Parado | Dashboard |
| 11:50 | "O Legal AI Copilot demonstra um fluxo completo..." | Move-se para navbar | Dashboard |
| 11:53 | [Fala sobre fluxo] | Parado na navbar | Dashboard |
| 11:56 | [Fala final] | Move-se ao centro | Dashboard |
| 12:00 | [Fala final] | Parado no centro | Dashboard |
| 12:05 | [Fala final] | Move-se a posição neutra | Dashboard |
| 12:07 | [Silêncio 2s] | Parado | Dashboard |
| 12:09 | [Silêncio] | Parado | Dashboard |
| 12:25 | [Fade out] | — | Fade to black |

**Ritmo**: Lento. Pausas de 1s entre tópicos. Cursor quase parado. Tela estática predominante.

---

## 3. Tempo de Leitura Visual

### Fórmula

```
Tempo de leitura = (número de palavras no elemento ÷ 3) + 1s de buffer
```

### Tempos Calculados por Elemento

| Elemento | Palavras (aprox.) | Tempo de leitura | Buffer | Total |
|----------|-------------------|-----------------|--------|-------|
| Card de resumo | 40–60 | 15–20s | 1s | 16–21s |
| Card "Partes Envolvidas" | 10–20 | 4–7s | 1s | 5–8s |
| Card "Datas Importantes" | 5–10 | 2–3s | 1s | 3–4s |
| Card "Valores" | 5–10 | 2–3s | 1s | 3–4s |
| Card "Cláusulas Importantes" | 15–25 | 5–8s | 1s | 6–9s |
| Resposta do chat | 50–80 | 17–27s | 1s | 18–28s |
| Citações | 10–20 | 4–7s | 1s | 5–8s |
| Disclaimer | 10–15 | 3–5s | 1s | 4–6s |
| Overall risk card | 5–10 | 2–3s | 1s | 3–4s |
| Risk card individual | 20–30 | 7–10s | 1s | 8–11s |
| Sources expandidas | 15–25 | 5–8s | 1s | 6–9s |
| Card de automação | 10–15 | 3–5s | 1s | 4–6s |
| Painel de detalhe (revisão) | 20–40 | 7–13s | 1s | 8–14s |
| Histórico de revisões | 10–20 | 4–7s | 1s | 5–8s |
| 4 cards de métricas | 4–8 (números) | 2–3s | 1s | 3–4s |
| Grid 2x2 (métricas) | 10–20 | 4–7s | 1s | 5–8s |
| Estimativa de produtividade | 10–15 | 3–5s | 1s | 4–6s |
| Resultado da comparação | 30–50 | 10–17s | 1s | 11–18s |

> **Nota**: O tempo de leitura é o tempo mínimo que o cursor deve permanecer parado sobre o elemento. Se a fala durar mais, aguardar a fala terminar antes de mover.

---

## 4. Sincronização de Mudança de Página

### Quando Mudar de Página

A mudança de página (navegação via navbar ou botão) deve ocorrer **imediatamente após** a fala indicar a ação. Não há pausa entre fala e clique.

### Sequência Padrão

```
1. Fala menciona a funcionalidade/próxima tela
2. Cursor move-se para o botão/navbar (1–2s)
3. Pausa de 500ms (cursor parado sobre o botão)
4. Clique
5. Página carrega (aguardar completamente)
6. Cursor para em posição neutra
7. Fala continua descrevendo a nova tela
```

### Exemplo (Cena 05 → 06)

```
02:49  Fala: "...vamos fazer o upload de um novo contrato"
02:49  Cursor move-se para "Upload PDF"
02:52  Cursor parado sobre "Upload PDF" (500ms)
02:53  Clique
02:53  Página /upload carregando
02:55  Página carregada
02:55  Cursor para no centro
02:56  Fala: "Vou fazer o upload de um contrato..."
```

---

## 5. Sincronização de Scroll

### Quando Fazer Scroll

O scroll deve ocorrer **após** a fala mencionar o conteúdo abaixo ou **após** o tempo de leitura do conteúdo atual completar.

### Sequência Padrão

```
1. Fala descreve o conteúdo visível
2. Tempo de leitura (cursor parado)
3. Fala menciona conteúdo abaixo: "Abaixo, temos..."
4. Scroll suave (1–2s)
5. Cursor para (2s de leitura do novo conteúdo)
6. Fala continua descrevendo o novo conteúdo
```

### Exemplo (Cena 07)

```
04:15  Fala: "O resumo é gerado automaticamente..."
04:18  Fala: "Abaixo, temos quatro cards..."
04:18  Scroll para baixo (~400px, 2s)
04:20  Novo conteúdo visível (grid 2x2)
04:20  Cursor para (2s de leitura)
04:22  Fala: "As partes identificadas incluem..."
```

---

## 6. Pausas e Silêncios

### Pausas Respiradas (na fala)

| Tipo | Duração | Quando |
|------|---------|--------|
| Pausa curta | 300–500ms | Entre frases da mesma ideia |
| Pausa média | 1s | Entre ideias diferentes |
| Pausa longa | 2s | Entre tópicos ou seções |
| Silêncio inicial | 3s | Início do vídeo (Cena 01) |
| Silêncio final | 2s | Fim de cada cena |

### Silêncios com Cursor Parado

| Momento | Duração | Cursor |
|---------|---------|--------|
| Antes do primeiro clique da cena | 500ms | Parado sobre o botão |
| Após carregamento de página | 2s | Parado em posição neutra |
| Após carregamento de resultado | 3s | Parado em posição neutra |
| Frame final de cada cena | 2–3s | Parado em posição neutra |
| Durante loading | Até completar | Parado (NÃO mover) |

---

## 7. Velocidade de Fala Recomendada

| Cena | Velocidade | Palavras/min |
|------|-----------|-------------|
| 01 — Abertura | Lenta | 120–140 |
| 02 — Problema | Moderada | 140–160 |
| 03 — Arquitetura | Moderada | 140–160 |
| 04 — Login | Moderada | 140–160 |
| 05 — Dashboard | Moderada | 140–160 |
| 06 — Upload | Moderada | 140–160 |
| 07 — Análise | Moderada | 140–160 |
| 08 — Chat | Moderada | 140–160 |
| 09 — Riscos | Moderada | 140–160 |
| 10 — Automações | Rápida | 160–180 |
| 11 — Revisões | Moderada | 140–160 |
| 12 — Métricas | Rápida | 160–180 |
| 13 — Comparação | Rápida | 160–180 |
| 14 — Encerramento | Lenta | 120–140 |

> **Nota**: A velocidade de fala deve ser natural e clara. Não acelerar artificialmente — cortes de silêncio na edição são preferíveis a fala acelerada.
