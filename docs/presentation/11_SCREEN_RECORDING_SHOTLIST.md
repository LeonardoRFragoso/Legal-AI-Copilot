# Shot List Cinematográfico — Legal AI Copilot

> Documento frame a frame para gravação de tela.
> Sem webcam. Sem apresentador. Apenas tela, cursor e narração em off.
> Estilo: Stripe, Vercel, Supabase, Linear, GitHub, OpenAI.
> Este documento deve ser seguido literalmente. Nada depende de improvisação.

---

## Objetivo

Este é o shot list definitivo para a gravação da tela do vídeo de apresentação do Legal AI Copilot. Cada cena, cada movimento de cursor, cada clique, cada espera e cada scroll estão documentados com precisão. O operador de gravação deve seguir este documento como um roteiro técnico — sem desvios, sem improvisação.

O vídeo resultante deve transmitir profissionalismo, clareza e fluidez, no estilo de apresentações técnicas de empresas como Stripe, Vercel e Linear.

---

## Regras Gerais

1. **Cursor sempre visível** — nunca ocultar o cursor do mouse em nenhuma cena.
2. **Movimentos suaves** — todo movimento de cursor deve ser linear e constante, sem acelerações bruscas.
3. **Nunca mover rapidamente** — velocidade máxima de cursor: ~250 pixels/segundo.
4. **Nunca fazer movimentos desnecessários** — o cursor só se move quando há um motivo (apontar, clicar, navegar).
5. **Nunca clicar repetidamente** — um clique por ação. Se o clique não registrou, aguardar 1s e tentar novamente (mas editar o erro na pós-produção).
6. **Evitar scroll exagerado** — scroll apenas quando necessário para revelar conteúdo. Nunca scroll de ida e volta.
7. **Esperar animações terminarem** — nunca clicar ou mover durante uma animação de transição ou loading.
8. **Esperar carregamentos** — aguardar completamente qualquer loading spinner antes de prosseguir.
9. **Nunca deixar o cursor "procurando" um botão** — o cursor deve saber para onde vai. Movimento direto e confiante.
10. **Cursor parado em local neutro** quando não estiver apontando nada — canto inferior direito da área de conteúdo (aprox. x:1700, y:950).

---

## Configuração do Navegador

| Parâmetro | Valor |
|-----------|-------|
| Navegador | Google Chrome (versão estável) |
| Perfil | Perfil limpo exclusivo ("Demo Profile") |
| Resolução do monitor | 1920×1080 |
| Tamanho da janela | Maximizada |
| Zoom do navegador | 100% (Ctrl+0) |
| Tema | Claro (Light mode) |
| Abas abertas | 1 aba apenas — a aplicação |
| Barra de favoritos | Oculta (Ctrl+Shift+B) |
| Extensões | Nenhuma visível na barra |
| Downloads | Nenhum ativo. Barra de downloads fechada |
| Notificações | Desabilitadas (chrome://settings/content/notifications) |
| Histórico | Limpo |
| Cache | Limpo |
| Preenchimento automático | Desabilitado |
| URL inicial | `http://localhost:5173/login` |

### Sistema Operacional

| Parâmetro | Valor |
|-----------|-------|
| "Não perturbe" | Ativado |
| Notificações de apps | Desabilitadas |
| Dock/Barra de tarefas | Auto-ocultar |
| Papel de parede | Cor sólida neutra (#333333) |
| Ícones do desktop | Removidos |
| Escala/DPI | 100% |

---

## Shot List Completa

> **Sistema de coordenadas**: 1920×1080. Origem (0,0) no canto superior esquerdo.
> A navbar da aplicação ocupa aproximadamente y:0–64. Conteúdo começa em y:64.
> Todas as coordenadas são aproximadas (±20px) e referem-se ao centro do elemento alvo.

---

### CENA 01 — Título / Abertura

| Campo | Valor |
|------|-------|
| **Cena** | 01 |
| **Objetivo** | Apresentar o projeto com tela estática e narração em off |
| **Tempo inicial** | 00:00:00 |
| **Tempo final** | 00:00:30 |
| **Tela** | Tela de login do Legal AI Copilot |
| **URL** | `http://localhost:5173/login` |
| **Elemento principal** | Logo da balança + título "Legal AI Copilot" |

#### Ações

```
01. Tela de login carregada e estática
    Cursor parado em posição neutra (x:960, y:540 — centro da tela)
    Esperar: 3 segundos (tela estática antes da narração)

02. Mover cursor lentamente para o logo da balança (x:960, y:300)
    Velocidade: ~150px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (cursor parado sobre o logo)

03. Mover cursor lentamente para o título "Legal AI Copilot" (x:960, y:350)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (cursor parado sob o título)

04. Mover cursor lentamente de volta ao centro (x:960, y:540)
    Velocidade: ~150px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (tela estática, cursor parado)

05. Mover cursor lentamente para a seção "Credenciais de demonstração" (x:960, y:680)
    Velocidade: ~150px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (cursor parado, mostrando as credenciais demo)

06. Mover cursor de volta ao centro (x:960, y:540)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (tela estática para transição)
```

#### Checklist da Cena 01
- [ ] Cursor parado no centro
- [ ] Tela de login carregada
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] Nenhum clique errado
- [ ] Movimentos suaves

---

### CENA 02 — Problema e Contexto

| Campo | Valor |
|------|-------|
| **Cena** | 02 |
| **Objetivo** | Narrar o problema enquanto a tela de login permanece visível |
| **Tempo inicial** | 00:00:30 |
| **Tempo final** | 00:01:15 |
| **Tela** | Tela de login (mesma da Cena 01) |
| **URL** | `http://localhost:5173/login` |
| **Elemento principal** | Formulário de login (campos email/senha) |

#### Ações

```
01. Tela de login estática (continuação da Cena 01)
    Cursor parado no centro (x:960, y:540)
    Esperar: 5 segundos (narração do problema)

02. Mover cursor lentamente para o campo de email (x:960, y:430)
    Velocidade: ~100px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (cursor parado sobre o campo email)

03. Mover cursor lentamente para o campo de senha (x:960, y:510)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (cursor parado sobre o campo senha)

04. Mover cursor lentamente para o botão "Entrar" (x:960, y:580)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (cursor parado sobre o botão)

05. Mover cursor de volta ao centro (x:960, y:540)
    Velocidade: ~150px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 5 segundos (tela estática, narração sobre a solução)

06. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (preparação para transição)
```

#### Checklist da Cena 02
- [ ] Cursor parado no centro
- [ ] Tela de login estável
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] Nenhum clique
- [ ] Movimentos suaves

---

### CENA 03 — Arquitetura

| Campo | Valor |
|------|-------|
| **Cena** | 03 |
| **Objetivo** | Narrar a arquitetura enquanto a tela de login permanece visível |
| **Tempo inicial** | 00:01:15 |
| **Tempo final** | 00:02:00 |
| **Tela** | Tela de login (mesma) |
| **URL** | `http://localhost:5173/login` |
| **Elemento principal** | Credenciais demo (botões Advogado/Admin) |

#### Ações

```
01. Tela de login estática (continuação)
    Cursor em posição neutra (x:1700, y:950)
    Esperar: 3 segundos (início da narração de arquitetura)

02. Mover cursor lentamente para o botão "Advogado" (x:960, y:680)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (cursor sobre o botão Advogado — narração sobre RBAC)

03. Mover cursor lentamente para o botão "Admin" (x:960, y:740)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (cursor sobre o botão Admin — narração sobre papéis)

04. Mover cursor de volta ao centro (x:960, y:540)
    Velocidade: ~150px/s
    Duração do movimento: ~2 segundos
    Esperar: 5 segundos (narração sobre agent router e guardrails)

05. Mover cursor para o botão "Entrar" (x:960, y:580)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 2 segundos (preparação para clique na Cena 04)
```

#### Checklist da Cena 03
- [ ] Cursor parado no botão "Entrar" ao final
- [ ] Tela de login estável
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] Nenhum clique
- [ ] Movimentos suaves

---

### CENA 04 — Login

| Campo | Valor |
|------|-------|
| **Cena** | 04 |
| **Objetivo** | Realizar login e demonstrar autenticação JWT com RBAC |
| **Tempo inicial** | 00:02:00 |
| **Tempo final** | 00:02:30 |
| **Tela** | Login → Dashboard |
| **URL** | `http://localhost:5173/login` → `http://localhost:5173/dashboard` |
| **Elemento principal** | Botão "Advogado" (credenciais demo) e botão "Entrar" |

#### Ações

```
01. Tela de login carregada
    Cursor parado sobre o botão "Entrar" (x:960, y:580) — herdado da Cena 03
    Esperar: 1 segundo

02. Mover cursor lentamente para o botão "Advogado" (x:960, y:680)
    Velocidade: ~100px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms (pausa antes do clique)

03. Clicar no botão "Advogado"
    — Campos email e senha preenchem automaticamente
    Esperar: 1.5 segundos (campos preenchidos visíveis)

04. Mover cursor lentamente para o botão "Entrar" (x:960, y:580)
    Velocidade: ~100px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms (pausa antes do clique)

05. Clicar no botão "Entrar"
    — Botão mostra "Entrando..."
    Esperar carregamento: 2–3 segundos (aguardar redirect para dashboard)

06. Dashboard carregado e estático
    Cursor parado em posição neutra (x:960, y:540)
    Esperar: 3 segundos (dashboard visível, narração sobre JWT e RBAC)
```

#### Checklist da Cena 04
- [ ] Cursor parado no botão "Advogado" antes de clicar
- [ ] Campos preenchidos após clique
- [ ] Cursor parado no botão "Entrar" antes de clicar
- [ ] Dashboard carregado completamente
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] 2 cliques executados
- [ ] Movimentos suaves

---

### CENA 05 — Dashboard

| Campo | Valor |
|------|-------|
| **Cena** | 05 |
| **Objetivo** | Mostrar a lista de documentos e a barra de navegação |
| **Tempo inicial** | 00:02:30 |
| **Tempo final** | 00:03:00 |
| **Tela** | Dashboard |
| **URL** | `http://localhost:5173/dashboard` |
| **Elemento principal** | Navbar (9 itens) + cards de documentos |

#### Ações

```
01. Dashboard carregado e estático
    Cursor parado no centro (x:960, y:540)
    Esperar: 2 segundos (tela estável, início da narração)

02. Mover cursor lentamente para a navbar — item "Dashboard" (x:200, y:32)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms (pausa sobre "Dashboard")

03. Mover cursor lentamente pela navbar, parando em cada item:
    - "Upload" (x:310, y:32) — esperar 300ms
    - "Chat" (x:400, y:32) — esperar 300ms
    - "Análise" (x:480, y:32) — esperar 300ms
    - "Riscos" (x:570, y:32) — esperar 300ms
    - "Automações" (x:660, y:32) — esperar 300ms
    - "Revisões" (x:770, y:32) — esperar 300ms
    - "Métricas" (x:870, y:32) — esperar 300ms
    - "Comparação" (x:970, y:32) — esperar 300ms
    Velocidade: ~300px/s entre itens
    Duração total: ~5 segundos

04. Mover cursor para o nome do usuário / role badge no canto direito (x:1750, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (nome e role visíveis)

05. Mover cursor para o primeiro card de documento (x:300, y:300)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (card visível — título, status, botões)

06. Mover cursor para o botão "Análise" no card (x:380, y:420)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms (preparação para navegação — não clicar aqui)

07. Mover cursor para o botão "Upload PDF" no canto superior direito (x:1650, y:120)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms (pausa antes do clique)

08. Clicar no botão "Upload PDF"
    — Navegação para /upload
    Esperar carregamento: 2 segundos (página de upload carregando)
```

#### Checklist da Cena 05
- [ ] Dashboard carregado com documentos
- [ ] Cursor percorreu todos os 9 itens da navbar
- [ ] Cursor parou no nome/role do usuário
- [ ] Cursor parou no primeiro card
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] 1 clique (Upload PDF)
- [ ] Movimentos suaves pela navbar

---

### CENA 06 — Upload de Contrato

| Campo | Valor |
|------|-------|
| **Cena** | 06 |
| **Objetivo** | Demonstrar o upload com processamento automático |
| **Tempo inicial** | 00:03:00 |
| **Tempo final** | 00:04:00 |
| **Tela** | Upload → Dashboard (após sucesso) |
| **URL** | `http://localhost:5173/upload` → `http://localhost:5173/dashboard` |
| **Elemento principal** | Formulário de upload + tela de sucesso |

#### Ações

```
01. Página de upload carregada e estática
    Cursor parado no centro do formulário (x:960, y:400)
    Esperar: 2 segundos (tela estável, início da narração)

02. Mover cursor para o campo "Título do Documento" (x:960, y:300)
    Velocidade: ~150px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms (pausa antes do clique)

03. Clicar no campo "Título do Documento"
    — Campo focado
    Esperar: 500ms

04. Digitar: "Contrato de Prestação de Serviços — Demo"
    Velocidade de digitação: natural (~60 palavras/min)
    Duração: ~4 segundos
    Esperar: 500ms (título preenchido visível)

05. Mover cursor para a área de upload (drop zone) (x:960, y:450)
    Velocidade: ~150px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms (pausa antes do clique)

06. Clicar na área de upload
    — File picker abre
    Esperar: 1 segundo (file picker visível)

07. Selecionar arquivo: Contrato_Prestacao_Servicos_Teste.pdf
    — Navegar até o arquivo no file picker e clicar
    — File picker fecha
    — Nome do arquivo visível na drop zone
    Esperar: 2 segundos (nome do arquivo visível)

08. Mover cursor para o botão "Fazer Upload" (x:960, y:650)
    Velocidade: ~150px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms (pausa antes do clique)

09. Clicar no botão "Fazer Upload"
    — Botão mostra "Processando..."
    Esperar carregamento: aguardar completamente (3–8 segundos)
    — NÃO clicar nada durante o processamento
    — NÃO mover o cursor durante o processamento

10. Tela de sucesso visível (CheckCircle verde + "Upload realizado com sucesso!")
    Cursor parado (não mover)
    Esperar: 3 segundos (tela de sucesso visível)

11. Redirect automático para dashboard
    — Dashboard carregado com novo documento
    Cursor parado em posição neutra (x:960, y:540)
    Esperar: 3 segundos (dashboard com novo documento visível)
```

#### Checklist da Cena 06
- [ ] Campo de título preenchido
- [ ] Arquivo PDF selecionado
- [ ] Botão "Fazer Upload" clicado
- [ ] Loading aguardado completamente
- [ ] Tela de sucesso visível por 3s
- [ ] Dashboard com novo documento
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~60s)
- [ ] 3 cliques (campo, drop zone, botão)
- [ ] Cursor parado durante loading

---

### CENA 07 — Análise (Resumo + Extração)

| Campo | Valor |
|------|-------|
| **Cena** | 07 |
| **Objetivo** | Mostrar resumo automático e extração estruturada |
| **Tempo inicial** | 00:04:00 |
| **Tempo final** | 00:05:30 |
| **Tela** | Análise de Contrato |
| **URL** | `http://localhost:5173/analysis` (ou `?doc={id}`) |
| **Elemento principal** | Card de resumo + grid 2x2 de extração |

#### Ações

```
01. Mover cursor para "Análise" na navbar (x:480, y:32)
    Velocidade: ~300px/s (a partir do dashboard)
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Análise" na navbar
    — Navegação para /analysis
    Esperar carregamento: 2–3 segundos (página carregando)

03. Página de análise carregada
    — Se documento já estiver selecionado: ir para passo 05
    — Se dropdown visível: ir para passo 04
    Cursor parado no centro (x:960, y:200)
    Esperar: 1 segundo

04. Mover cursor para o dropdown de documentos (x:1500, y:120)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms
    Clicar no dropdown
    Esperar: 500ms (lista aberta)
    Mover cursor para o documento desejado na lista (x:1500, y:180)
    Velocidade: ~100px/s
    Esperar: 500ms
    Clicar no documento
    Esperar: 500ms

05. Loading spinner visível ("Analisando documento...")
    Cursor parado em posição neutra (x:1700, y:950)
    Esperar carregamento: aguardar completamente (3–8 segundos)
    — NÃO mover o cursor durante o loading

06. Análise carregada — card de Resumo visível
    Cursor parado (x:1700, y:950)
    Esperar: 3 segundos (resumo visível para leitura)

07. Mover cursor lentamente para o card de Resumo (x:960, y:250)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (texto do resumo visível)

08. Mover cursor para o botão "Iniciar Chat" (x:1500, y:250)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 1 segundo (botão visível — não clicar ainda)

09. Realizar scroll para baixo: aproximadamente 400 pixels
    Velocidade: suave (~200px/s)
    Duração: ~2 segundos
    Esperar: 2 segundos (grid 2x2 visível)

10. Mover cursor para o card "Partes Envolvidas" (x:400, y:500)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (conteúdo do card visível)

11. Mover cursor para o card "Datas Importantes" (x:1400, y:500)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (conteúdo do card visível)

12. Mover cursor para o card "Valores" (x:400, y:800)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (conteúdo do card visível)

13. Mover cursor para o card "Cláusulas Importantes" (x:1400, y:800)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (badges de risco visíveis)

14. Mover cursor lentamente sobre os badges de risco no card de Cláusulas
    — Passar o cursor sobre cada badge (Baixo/Médio/Alto)
    Velocidade: ~100px/s
    Duração: ~3 segundos
    Esperar: 2 segundos (badges visíveis)

15. Mover cursor de volta ao botão "Iniciar Chat" (x:1500, y:250)
    Realizar scroll para cima: aproximadamente 600 pixels
    Velocidade: suave (~200px/s)
    Duração: ~3 segundos
    Esperar: 1 segundo (botão "Iniciar Chat" visível novamente)
```

#### Checklist da Cena 07
- [ ] Documento selecionado no dropdown
- [ ] Loading aguardado completamente
- [ ] Card de resumo visível por 3s
- [ ] Scroll suave para grid 2x2
- [ ] Cada card de extração visitado
- [ ] Badges de risco apontados
- [ ] Cursor parado em "Iniciar Chat" ao final
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~90s)
- [ ] 2–3 cliques (navbar, dropdown se necessário)
- [ ] 1 scroll para baixo, 1 scroll para cima

---

### CENA 08 — Chat com Agent Router

| Campo | Valor |
|------|-------|
| **Cena** | 08 |
| **Objetivo** | Demonstrar chat com roteamento de intenção e guardrails |
| **Tempo inicial** | 00:05:30 |
| **Tempo final** | 00:07:00 |
| **Tela** | Chat |
| **URL** | `http://localhost:5173/chat` (ou `?conv={id}` via "Iniciar Chat") |
| **Elemento principal** | Interface de chat + resposta estruturada com citações |

#### Ações

```
01. Clicar no botão "Iniciar Chat" (x:1500, y:250)
    — Navegação para /chat?conv={id}
    Esperar carregamento: 2–3 segundos (chat carregando)

02. Tela de chat carregada
    — Sidebar à esquerda com lista de conversas
    — Área principal de mensagens
    Cursor parado no centro (x:960, y:540)
    Esperar: 2 segundos (tela estável)

03. Mover cursor para a sidebar — botão "Nova Conversa" (x:150, y:120)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (botão visível — não clicar se conversa já existe)

04. Mover cursor para a conversa mais recente na sidebar (x:150, y:200)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 2 segundos (conversa destacada)

05. Mover cursor para o campo de texto (x:960, y:950)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms (pausa antes do clique)

06. Clicar no campo de texto
    — Campo focado
    Esperar: 500ms

07. Digitar: "Quais são os riscos deste contrato?"
    Velocidade de digitação: natural (~60 palavras/min)
    Duração: ~3 segundos
    Esperar: 500ms (texto visível no campo)

08. Mover cursor para o botão Send (x:1750, y:950)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms (pausa antes do clique)

09. Clicar no botão Send
    — Mensagem enviada (balão azul à direita)
    Esperar: 1 segundo (mensagem visível)

10. Aguardar resposta do assistente
    Cursor parado em posição neutra (x:1700, y:950)
    — NÃO mover o cursor durante o loading
    Esperar carregamento: aguardar completamente (3–10 segundos)
    — Resposta aparece (balão cinza à esquerda)

11. Resposta do assistente visível
    Cursor parado (x:1700, y:950)
    Esperar: 3 segundos (resposta visível para leitura)

12. Mover cursor lentamente para a resposta do assistente (x:800, y:600)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (riscos estruturados visíveis — RiskBadge, título, descrição)

13. Mover cursor para as citações abaixo da resposta (x:800, y:800)
    Velocidade: ~100px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 3 segundos (citações visíveis — página, trecho, similarity)

14. Realizar scroll para baixo: aproximadamente 200 pixels (se necessário para ver disclaimer)
    Velocidade: suave
    Duração: ~1 segundo
    Esperar: 1 segundo

15. Mover cursor para o disclaimer (x:800, y:900)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (disclaimer visível em itálico cinza)

16. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (tela estática para transição)
```

#### Checklist da Cena 08
- [ ] Conversa selecionada ou criada
- [ ] Pergunta digitada corretamente
- [ ] Botão Send clicado
- [ ] Resposta aguardada completamente
- [ ] Resposta estruturada visível por 3s
- [ ] Citações apontadas
- [ ] Disclaimer apontado
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~90s)
- [ ] 2 cliques (campo de texto, Send)
- [ ] Cursor parado durante loading

---

### CENA 09 — Análise de Riscos

| Campo | Valor |
|------|-------|
| **Cena** | 09 |
| **Objetivo** | Demonstrar análise heurística de riscos contratuais |
| **Tempo inicial** | 00:07:00 |
| **Tempo final** | 00:08:30 |
| **Tela** | Análise de Riscos |
| **URL** | `http://localhost:5173/risks` (ou `?doc={id}`) |
| **Elemento principal** | Overall risk card + risk cards + Sources expansíveis |

#### Ações

```
01. Mover cursor para "Riscos" na navbar (x:570, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Riscos" na navbar
    — Navegação para /risks
    Esperar carregamento: 2–3 segundos

03. Página de riscos carregada
    — Se documento já estiver selecionado: ir para passo 05
    — Se dropdown visível: ir para passo 04
    Cursor parado no centro (x:960, y:200)
    Esperar: 1 segundo

04. Mover cursor para o dropdown de documentos (x:1500, y:120)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms
    Clicar no dropdown
    Esperar: 500ms
    Mover cursor para o documento (x:1500, y:180)
    Clicar no documento
    Esperar: 500ms

05. Card inicial visível com botão "Analyze Risks"
    Cursor parado no centro (x:960, y:300)
    Esperar: 2 segundos (tela estável, narração)

06. Mover cursor para o botão "Analyze Risks" (x:960, y:400)
    Velocidade: ~150px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms (pausa antes do clique)

07. Clicar no botão "Analyze Risks"
    — Análise iniciada
    Esperar carregamento: aguardar completamente (3–8 segundos)
    — NÃO mover o cursor durante o loading

08. Resultado carregado — Overall Risk card visível
    Cursor parado (x:1700, y:950)
    Esperar: 3 segundos (overall risk visível para leitura)

09. Mover cursor para o Overall Risk card (x:960, y:300)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (número de risk, confidence score, level visíveis)

10. Mover cursor para o primeiro risk card (x:960, y:500)
    Velocidade: ~150px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 3 segundos (severidade, categoria, descrição, recomendação visíveis)

11. Mover cursor para o botão "Sources" no primeiro risk card (x:1100, y:600)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms (pausa antes do clique)

12. Clicar no botão "Sources"
    — Sources expandem mostrando excerpt e similarity
    Esperar: 2 segundos (sources expandidas visíveis)

13. Mover cursor para o conteúdo expandido de Sources (x:960, y:700)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (excerpt, page number, similarity score visíveis)

14. Realizar scroll para baixo: aproximadamente 300 pixels (para ver mais risk cards se houver)
    Velocidade: suave
    Duração: ~1.5 segundos
    Esperar: 2 segundos (mais cards visíveis)

15. Mover cursor para o disclaimer ao final da página (x:960, y:900)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (disclaimer visível — narração sobre heurística)

16. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (tela estática para transição)
```

#### Checklist da Cena 09
- [ ] Documento selecionado
- [ ] Botão "Analyze Risks" clicado
- [ ] Loading aguardado completamente
- [ ] Overall risk card visível por 3s
- [ ] Risk card apontado
- [ ] Sources expandidas
- [ ] Disclaimer apontado
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~90s)
- [ ] 2–3 cliques (navbar/dropdown, Analyze Risks, Sources)
- [ ] 1 scroll para baixo

---

### CENA 10 — Automações

| Campo | Valor |
|------|-------|
| **Cena** | 10 |
| **Objetivo** | Mostrar o pipeline de automação pós-upload com webhook |
| **Tempo inicial** | 00:08:30 |
| **Tempo final** | 00:09:15 |
| **Tela** | Automações |
| **URL** | `http://localhost:5173/automations` |
| **Elemento principal** | Lista de runs com status, progresso e webhook |

#### Ações

```
01. Mover cursor para "Automações" na navbar (x:660, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Automações" na navbar
    — Navegação para /automations
    Esperar carregamento: 2–3 segundos

03. Página de automações carregada
    Cursor parado no centro (x:960, y:200)
    Esperar: 2 segundos (lista de runs visível)

04. Mover cursor para o primeiro card de automação (x:960, y:300)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 3 segundos (status badge, step, barra de progresso visíveis)

05. Mover cursor para o status badge do primeiro run (x:300, y:300)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (status visível — COMPLETED/FAILED/PARTIAL_SUCCESS)

06. Mover cursor para a barra de progresso (x:600, y:350)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (barra de progresso visível)

07. Mover cursor para o webhook status (x:1400, y:350)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (webhook status visível — sent/failed/pending)

08. Mover cursor para o filtro de status (dropdown) (x:1500, y:120)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (filtro visível — não clicar)

09. Mover cursor para o botão "Atualizar" (x:1700, y:120)
    Velocidade: ~200px/s
    Duração do movimento: ~1 segundo
    Esperar: 1 segundo (botão visível — não clicar)

10. Realizar scroll para baixo: aproximadamente 300 pixels (se houver mais runs)
    Velocidade: suave
    Duração: ~1.5 segundos
    Esperar: 2 segundos (mais runs visíveis)

11. Mover cursor para o link "Ver documento" em um run (x:400, y:600)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (link visível)

12. Mover cursor para o link "Ver riscos" no mesmo run (x:600, y:600)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 2 segundos (link visível)

13. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 1 segundo (preparação para transição)
```

#### Checklist da Cena 10
- [ ] Lista de automações carregada
- [ ] Status badge apontado
- [ ] Barra de progresso apontada
- [ ] Webhook status apontado
- [ ] Filtro e botão Atualizar apontados
- [ ] Links "Ver documento" e "Ver riscos" apontados
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] 1 clique (navbar)
- [ ] 1 scroll para baixo

---

### CENA 11 — Revisão Humana

| Campo | Valor |
|------|-------|
| **Cena** | 11 |
| **Objetivo** | Demonstrar workflow de revisão humana com state machine |
| **Tempo inicial** | 00:09:15 |
| **Tempo final** | 00:10:15 |
| **Tela** | Revisão de Análises |
| **URL** | `http://localhost:5173/reviews` |
| **Elemento principal** | Lista de análises + painel de detalhe + formulário de revisão |

#### Ações

```
01. Mover cursor para "Revisões" na navbar (x:770, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Revisões" na navbar
    — Navegação para /reviews
    Esperar carregamento: 2–3 segundos

03. Página de revisões carregada
    — Lista de análises à esquerda
    — Painel de detalhe à direita (vazio ou com primeira análise)
    Cursor parado no centro (x:960, y:400)
    Esperar: 2 segundos (lista visível)

04. Mover cursor para o filtro de tipo (x:300, y:120)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 1 segundo (filtro visível — não clicar)

05. Mover cursor para o filtro de status (x:450, y:120)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 1 segundo (filtro visível — não clicar)

06. Mover cursor para o primeiro card na lista de análises (x:250, y:250)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (status badge, tipo, confiança, risco visíveis)

07. Clicar no primeiro card da lista
    — Painel de detalhe abre à direita
    Esperar carregamento: 1–2 segundos

08. Painel de detalhe carregado
    Cursor parado (x:1700, y:950)
    Esperar: 3 segundos (conteúdo do detalhe visível — tipo, status, metadata)

09. Mover cursor para o conteúdo do detalhe (x:900, y:300)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (content_summary, structured_result visíveis)

10. Realizar scroll para baixo: aproximadamente 300 pixels (para ver histórico e formulário)
    Velocidade: suave
    Duração: ~1.5 segundos
    Esperar: 2 segundos (histórico de revisões visível)

11. Mover cursor para o histórico de revisões (x:900, y:600)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 3 segundos (histórico visível — decision, reviewer, comment, date)

12. Mover cursor para o botão "Aprovar" (x:700, y:850)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms (pausa antes do clique)

13. Clicar no botão "Aprovar"
    — Botão selecionado (destaque)
    Esperar: 1 segundo (formulário de comentário visível)

14. Mover cursor para o campo de comentário (x:900, y:900)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms

15. Clicar no campo de comentário
    — Campo focado
    Esperar: 500ms

16. Digitar: "Análise correta, cláusulas identificadas adequadamente"
    Velocidade: natural (~60 palavras/min)
    Duração: ~3 segundos
    Esperar: 500ms

17. Mover cursor para o botão "Confirmar Revisão" (x:900, y:980)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 500ms (pausa antes do clique)

18. Clicar no botão "Confirmar Revisão"
    — Revisão enviada, histórico atualizado
    Esperar carregamento: 1–2 segundos

19. Histórico atualizado visível
    Cursor parado (x:1700, y:950)
    Esperar: 3 segundos (histórico atualizado com nova revisão visível)
```

#### Checklist da Cena 11
- [ ] Lista de análises carregada
- [ ] Filtros apontados (não clicados)
- [ ] Análise selecionada na lista
- [ ] Painel de detalhe aberto
- [ ] Histórico de revisões visível
- [ ] Botão "Aprovar" clicado
- [ ] Comentário digitado
- [ ] "Confirmar Revisão" clicado
- [ ] Histórico atualizado visível
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~60s)
- [ ] 4 cliques (card, Aprovar, comentário, Confirmar)
- [ ] 1 scroll para baixo

---

### CENA 12 — Métricas de Impacto

| Campo | Valor |
|------|-------|
| **Cena** | 12 |
| **Objetivo** | Apresentar dashboard de métricas e estimativas de produtividade |
| **Tempo inicial** | 00:10:15 |
| **Tempo final** | 00:11:00 |
| **Tela** | Métricas de Impacto |
| **URL** | `http://localhost:5173/insights` |
| **Elemento principal** | 4 cards superiores + grid 2x2 + estimativa de produtividade |

#### Ações

```
01. Mover cursor para "Métricas" na navbar (x:870, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Métricas" na navbar
    — Navegação para /insights
    Esperar carregamento: 2–3 segundos

03. Dashboard de métricas carregado
    Cursor parado no centro (x:960, y:300)
    Esperar: 2 segundos (4 cards superiores visíveis)

04. Mover cursor para o primeiro card superior — Documentos (x:250, y:250)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (número de documentos visível)

05. Mover cursor para o segundo card — Análises Geradas (x:700, y:250)
    Velocidade: ~300px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (número de análises visível)

06. Mover cursor para o terceiro card — Tempo Poupado (x:1150, y:250)
    Velocidade: ~300px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (horas poupadas visível)

07. Mover cursor para o quarto card — Taxa de Aprovação (x:1600, y:250)
    Velocidade: ~300px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (percentual visível)

08. Realizar scroll para baixo: aproximadamente 300 pixels (para ver grid 2x2)
    Velocidade: suave
    Duração: ~1.5 segundos
    Esperar: 2 segundos (grid 2x2 visível)

09. Mover cursor para "Análises por Tipo" (x:400, y:600)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (barras horizontais visíveis)

10. Mover cursor para "Status das Revisões" (x:1400, y:600)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (lista de status visível)

11. Mover cursor para "Riscos por Severidade" (x:400, y:800)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (badges coloridos visíveis)

12. Mover cursor para "Automações por Status" (x:1400, y:800)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 2 segundos (lista de status visível)

13. Realizar scroll para baixo: aproximadamente 300 pixels (para ver estimativa)
    Velocidade: suave
    Duração: ~1.5 segundos
    Esperar: 2 segundos (card de estimativa visível)

14. Mover cursor para a estimativa de produtividade (x:960, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (tempo manual, tempo poupado, confiança média visíveis)

15. Mover cursor para o aviso em itálico (estimation_notice) (x:960, y:1020)
    Velocidade: ~100px/s
    Duração do movimento: ~1 segundo
    Esperar: 3 segundos (aviso visível — narração sobre estimativas do MVP)

16. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 1 segundo (preparação para transição)
```

#### Checklist da Cena 12
- [ ] Dashboard de métricas carregado
- [ ] 4 cards superiores apontados individualmente
- [ ] Grid 2x2 visitado
- [ ] Estimativa de produtividade apontada
- [ ] Aviso (estimation_notice) apontado
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] 1 clique (navbar)
- [ ] 2 scrolls para baixo

---

### CENA 13 — Comparação de Contratos

| Campo | Valor |
|------|-------|
| **Cena** | 13 |
| **Objetivo** | Demonstrar comparação entre dois documentos |
| **Tempo inicial** | 00:11:00 |
| **Tempo final** | 00:11:30 |
| **Tela** | Comparação de Contratos |
| **URL** | `http://localhost:5173/comparison` |
| **Elemento principal** | Seleção de 2 documentos + resultado da comparação |

#### Ações

```
01. Mover cursor para "Comparação" na navbar (x:970, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Comparação" na navbar
    — Navegação para /comparison
    Esperar carregamento: 2–3 segundos

03. Página de comparação carregada
    Cursor parado no centro (x:960, y:300)
    Esperar: 2 segundos (tela estável, narração)

04. Mover cursor para o dropdown "Documento A" (x:400, y:300)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms (pausa antes do clique)

05. Clicar no dropdown "Documento A"
    — Lista de documentos abre
    Esperar: 500ms

06. Mover cursor para o primeiro documento na lista (x:400, y:360)
    Velocidade: ~100px/s
    Duração do movimento: ~0.5 segundos
    Esperar: 500ms

07. Clicar no primeiro documento
    — Documento A selecionado
    Esperar: 1 segundo

08. Mover cursor para o dropdown "Documento B" (x:1400, y:300)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms (pausa antes do clique)

09. Clicar no dropdown "Documento B"
    — Lista de documentos abre
    Esperar: 500ms

10. Mover cursor para o segundo documento na lista (x:1400, y:360)
    Velocidade: ~100px/s
    Duração do movimento: ~0.5 segundos
    Esperar: 500ms

11. Clicar no segundo documento
    — Documento B selecionado
    Esperar: 1 segundo (ambos os documentos selecionados visíveis)

12. Mover cursor para o botão "Comparar Documentos" (x:960, y:450)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 500ms (pausa antes do clique)

13. Clicar no botão "Comparar Documentos"
    — Botão mostra "Comparando..."
    Esperar carregamento: aguardar completamente (3–8 segundos)
    — NÃO mover o cursor durante o loading

14. Resultado da comparação visível
    Cursor parado (x:1700, y:950)
    Esperar: 3 segundos (resultado visível para leitura)

15. Mover cursor para o resultado (x:960, y:600)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (texto formatado com semelhanças e diferenças visível)

16. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~1.5 segundos
    Esperar: 2 segundos (tela estática para transição)
```

#### Checklist da Cena 13
- [ ] Documento A selecionado
- [ ] Documento B selecionado (diferente de A)
- [ ] Botão "Comparar Documentos" clicado
- [ ] Loading aguardado completamente
- [ ] Resultado visível por 3s
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] 5 cliques (navbar, dropdown A, doc A, dropdown B, doc B, Comparar)
- [ ] Cursor parado durante loading

---

### CENA 14 — Encerramento

| Campo | Valor |
|------|-------|
| **Cena** | 14 |
| **Objetivo** | Encerrar com limitações e conclusão sobre tela estática |
| **Tempo inicial** | 00:11:30 |
| **Tempo final** | 00:12:30 |
| **Tela** | Dashboard (tela estática) |
| **URL** | `http://localhost:5173/dashboard` |
| **Elemento principal** | Dashboard com lista de documentos |

#### Ações

```
01. Mover cursor para "Dashboard" na navbar (x:200, y:32)
    Velocidade: ~300px/s
    Duração do movimento: ~2 segundos
    Esperar: 500ms

02. Clicar em "Dashboard" na navbar
    — Navegação para /dashboard
    Esperar carregamento: 2 segundos

03. Dashboard carregado e estático
    Cursor parado no centro (x:960, y:540)
    Esperar: 5 segundos (tela estática, narração sobre limitações)

04. Mover cursor lentamente para a navbar (x:500, y:32)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 3 segundos (navbar visível — narração sobre fluxo completo)

05. Mover cursor lentamente de volta ao centro (x:960, y:540)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 5 segundos (tela estática, narração sobre modo heurístico)

06. Mover cursor para posição neutra (x:1700, y:950)
    Velocidade: ~200px/s
    Duração do movimento: ~2 segundos
    Esperar: 5 segundos (tela estática, conclusão final)

07. Cursor parado em posição neutra
    — Aguardar fade out na edição
    Esperar: 3 segundos (silêncio final antes do fade)
```

#### Checklist da Cena 14
- [ ] Dashboard carregado e estático
- [ ] Cursor parado por longos períodos
- [ ] Movimentos mínimos e lentos
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~60s)
- [ ] 1 clique (navbar Dashboard)
- [ ] Nenhum scroll
- [ ] Tela estática predominante

---

## Tempo de Permanência

| Cena | Tela | Tempo mínimo | Tempo ideal | Tempo máximo |
|------|------|-------------|-------------|-------------|
| 01 | Login (título) | 25s | 30s | 35s |
| 02 | Login (problema) | 40s | 45s | 50s |
| 03 | Login (arquitetura) | 40s | 45s | 50s |
| 04 | Login → Dashboard | 25s | 30s | 35s |
| 05 | Dashboard | 25s | 30s | 35s |
| 06 | Upload | 50s | 60s | 70s |
| 07 | Análise | 80s | 90s | 100s |
| 08 | Chat | 80s | 90s | 100s |
| 09 | Riscos | 80s | 90s | 100s |
| 10 | Automações | 40s | 45s | 50s |
| 11 | Revisões | 55s | 60s | 65s |
| 12 | Métricas | 40s | 45s | 50s |
| 13 | Comparação | 25s | 30s | 35s |
| 14 | Dashboard (encerramento) | 55s | 60s | 70s |

---

## Scroll

| Cena | Página | Quantidade | Velocidade | Pontos de parada |
|------|--------|-----------|-----------|-----------------|
| 01 | Login | 0 | N/A | N/A |
| 02 | Login | 0 | N/A | N/A |
| 03 | Login | 0 | N/A | N/A |
| 04 | Login → Dashboard | 0 | N/A | N/A |
| 05 | Dashboard | 0 | N/A | N/A |
| 06 | Upload | 0 | N/A | N/A |
| 07 | Análise | ~400px para baixo, ~600px para cima | Suave (~200px/s) | Após resumo (parar em grid 2x2). Após cláusulas (parar em "Iniciar Chat") |
| 08 | Chat | ~200px para baixo (se necessário) | Suave | Após resposta (parar em disclaimer) |
| 09 | Riscos | ~300px para baixo | Suave | Após primeiro risk card (parar em mais cards / disclaimer) |
| 10 | Automações | ~300px para baixo (se houver mais runs) | Suave | Após primeiro run (parar em mais runs) |
| 11 | Revisões | ~300px para baixo | Suave | Após detalhe (parar em histórico e formulário) |
| 12 | Métricas | ~300px + ~300px para baixo | Suave | Após 4 cards (parar em grid 2x2). Após grid (parar em estimativa) |
| 13 | Comparação | 0 | N/A | N/A |
| 14 | Dashboard | 0 | N/A | N/A |

### Regras de Scroll

- **Velocidade**: Suave e constante (~200–300px/s)
- **Direção**: Apenas para baixo (exceto Cena 07 que volta para "Iniciar Chat")
- **Nunca**: Scroll de ida e volta na mesma cena (exceto Cena 07)
- **Nunca**: Scroll muito rápido (parece errático)
- **Sempre**: Parar após o scroll e esperar 2s antes de mover o cursor

---

## Cursor

### Velocidade

| Tipo de movimento | Velocidade | Contexto |
|-------------------|-----------|----------|
| Apontar elemento próximo | ~100px/s | Movimentos curtos dentro da mesma área |
| Navegar entre áreas | ~200px/s | Movimentos médios na tela |
| Mover para navbar | ~300px/s | Movimentos longos de volta ao topo |
| Durante digitação | N/A | Cursor parado no campo |
| Durante loading | 0px/s | Cursor completamente parado |

### Paradas e Micro Pausas

| Momento | Duração |
|---------|---------|
| Antes de clicar um botão | 500ms |
| Após clicar um botão | 500ms |
| Sobre um elemento sendo narrado | 2–3s |
| Entre movimentos de apontamento | 500ms–1s |
| Durante loading | Até completar (parado) |
| Frame final de cada cena | 2–3s |

### Tempo Antes e Após Cliques

| Ação | Antes do clique | Após o clique |
|------|----------------|---------------|
| Clicar botão na navbar | 500ms parado | 500ms parado, depois aguardar carregamento |
| Clicar botão de ação | 500ms parado | 500ms parado, depois aguardar resultado |
| Clicar dropdown | 500ms parado | 500ms parado, depois mover para opção |
| Clicar opção de dropdown | 500ms parado | 500ms parado, depois aguardar carregamento |
| Clicar campo de texto | 500ms parado | 500ms parado, depois iniciar digitação |

---

## Carregamentos

### Regras Gerais

- **Esperar completamente** — nunca clicar, mover ou scroll durante um loading.
- **Nunca cortar** na gravação — o loading completo deve ser capturado.
- **Cursor parado** em posição neutra (x:1700, y:950) durante todos os carregamentos.

### Carregamentos por Cena

| Cena | Elemento | Tempo estimado | Acelerável na edição? |
|------|----------|---------------|----------------------|
| 04 | Redirect login → dashboard | 2–3s | Sim, se >3s (cross dissolve 0.2s) |
| 05 | Dashboard carregando | 1–2s | Não (rápido) |
| 06 | Upload processando | 3–8s | Sim, se >5s (speed ramp ou jump cut) |
| 07 | Análise carregando (spinner) | 3–8s | Sim, se >5s (cross dissolve 0.2s) |
| 08 | Resposta do chat | 3–10s | Sim, se >8s (cross dissolve 0.2s) |
| 09 | Análise de riscos | 3–8s | Sim, se >5s (cross dissolve 0.2s) |
| 11 | Detalhe da análise | 1–2s | Não (rápido) |
| 11 | Confirmar revisão | 1–2s | Não (rápido) |
| 12 | Métricas carregando | 1–3s | Não (rápido) |
| 13 | Comparação processando | 3–8s | Sim, se >5s (cross dissolve 0.2s) |

### Quando É Permitido Acelerar na Edição

- Loading > 5s: Acelerar com speed ramp (300%) ou cortar o meio com cross dissolve 0.2s
- Loading > 10s: Cortar obrigatoriamente — manter 1s no início e 1s no fim
- **Nunca** acelerar loading < 3s (é natural e rápido)
- **Nunca** remover completamente um loading (sempre manter 1s no início e 1s no fim)

---

## Leitura Visual

Tempo que o espectador precisa para absorver o conteúdo de cada tela antes de o cursor se mover:

| Cena | Tela/Elemento | Tempo de absorção |
|------|---------------|-------------------|
| 01 | Logo + título "Legal AI Copilot" | 3s |
| 02 | Formulário de login (campos) | 3s |
| 03 | Credenciais demo (botões) | 3s |
| 04 | Dashboard carregado (primeira vista) | 3s |
| 05 | Navbar completa (9 itens) | 5s (percorrer) |
| 05 | Card de documento | 2s |
| 06 | Formulário de upload | 2s |
| 06 | Tela de sucesso | 3s |
| 07 | Card de resumo | 3s |
| 07 | Card "Partes Envolvidas" | 3s |
| 07 | Card "Datas Importantes" | 3s |
| 07 | Card "Valores" | 3s |
| 07 | Card "Cláusulas Importantes" + badges | 3s |
| 08 | Sidebar de conversas | 2s |
| 08 | Resposta do assistente (estruturada) | 3s |
| 08 | Citações | 3s |
| 08 | Disclaimer | 3s |
| 09 | Overall Risk card | 3s |
| 09 | Risk card (severidade, categoria, descrição, recomendação) | 3s |
| 09 | Sources expandidas | 3s |
| 09 | Disclaimer | 3s |
| 10 | Card de automação (status, step, progresso) | 3s |
| 10 | Webhook status | 2s |
| 10 | Links "Ver documento" / "Ver riscos" | 2s |
| 11 | Lista de análises (cards) | 2s |
| 11 | Painel de detalhe (metadata, conteúdo) | 3s |
| 11 | Histórico de revisões | 3s |
| 11 | Formulário de revisão (3 botões) | 2s |
| 11 | Histórico atualizado | 3s |
| 12 | 4 cards superiores (números) | 2s cada (8s total) |
| 12 | Grid 2x2 (4 visualizações) | 2s cada (8s total) |
| 12 | Estimativa de produtividade | 3s |
| 12 | Aviso (estimation_notice) | 3s |
| 13 | Seleção de documentos (A e B) | 2s |
| 13 | Resultado da comparação | 3s |
| 14 | Dashboard estático | 5s por parada |

---

## Destaques

Elementos que merecem maior permanência do cursor e tempo de leitura:

| Cena | Elemento | Razão | Tempo extra |
|------|----------|-------|------------|
| 05 | Navbar (9 itens) | Mostra a amplitude do sistema | +2s por item |
| 07 | Badges de risco nas cláusulas | Diferencial visual e técnico | +3s |
| 08 | Resposta estruturada do chat | Demonstra guardrails e agent router | +3s |
| 08 | Citações com page number | Evidência de rastreabilidade | +3s |
| 08 | Disclaimer jurídico | Transparência e guardrails | +3s |
| 09 | Overall Risk card | Resultado principal da análise | +3s |
| 09 | Sources expandidas | Evidência e rastreabilidade | +3s |
| 09 | Disclaimer (heurística) | Limitação consciente do MVP | +3s |
| 10 | Status badges (COMPLETED/FAILED) | Funcionamento do pipeline | +2s |
| 10 | Webhook status | Integração com n8n | +2s |
| 11 | Histórico de revisões (append-only) | Auditoria e rastreabilidade | +3s |
| 11 | Formulário de revisão (3 botões) | State machine visual | +2s |
| 12 | Aviso de estimativas | Transparência sobre limitações | +3s |
| 13 | Resultado da comparação | Funcionalidade diferencial | +3s |

---

## Transições

| De → Para | Tipo | Duração | Observação |
|-----------|------|---------|-----------|
| Início → Cena 01 | Fade in from black | 0.5s | Abertura suave |
| Cena 01 → 02 | Cut seco | 0s | Mesma tela, mesma posição |
| Cena 02 → 03 | Cut seco | 0s | Mesma tela, mesma posição |
| Cena 03 → 04 | Cut seco | 0s | Mesma tela, cursor já posicionado |
| Cena 04 → 05 | Cut seco | 0s | Dashboard já visível no fim da 04 |
| Cena 05 → 06 | Cut seco | 0s | Navegação para /upload é a transição |
| Cena 06 → 07 | Cut seco | 0s | Navegação para /analysis é a transição |
| Cena 07 → 08 | Cross dissolve | 0.3s | Transição via botão "Iniciar Chat" |
| Cena 08 → 09 | Cut seco | 0s | Navegação para /risks é a transição |
| Cena 09 → 10 | Cut seco | 0s | Navegação para /automations é a transição |
| Cena 10 → 11 | Cut seco | 0s | Navegação para /reviews é a transição |
| Cena 11 → 12 | Cut seco | 0s | Navegação para /insights é a transição |
| Cena 12 → 13 | Cut seco | 0s | Navegação para /comparison é a transição |
| Cena 13 → 14 | Cut seco | 0s | Navegação para /dashboard é a transição |
| Cena 14 → Fim | Fade out to black | 1.0s | Encerramento |

### Princípio de Transições

- **Cut seco** entre cenas de tela: a navegação da aplicação (mudança de URL) já é uma transição visual natural. Não é necessário dissolve.
- **Cross dissolve 0.3s** apenas na Cena 07→08 (transição via botão "Iniciar Chat" que muda contexto de análise para chat).
- **Fade in/out** apenas no início e fim do vídeo.
- **Sem transições chamativas**: sem wipes, slides, zooms de transição.

---

## Continuidade

### Caso seja Necessário Regravar uma Única Cena

#### Antes de Regravar

1. **Restaurar o estado da aplicação**:
   - Navegar para a URL correta da cena
   - Selecionar o mesmo documento/conversa/análise
   - Aplicar os mesmos filtros (se houver)
   - Verificar que os dados na tela são idênticos

2. **Posicionar o cursor**:
   - Na posição inicial indicada no shot list da cena
   - Verificar que a posição é consistente com o frame final da cena anterior

3. **Sincronizar com a narração**:
   - Ter o roteiro de fala (`04_VIDEO_SPEECH_SCRIPT.md`) à mão
   - Iniciar a narração no ponto correto da cena

#### Como Esconder Cortes na Edição

| Situação | Técnica |
|----------|---------|
| Corte entre mesma tela, mesmo estado | Cut seco (invisível) |
| Corte entre mesma tela, estado diferente | Cross dissolve 0.3s |
| Corte entre telas diferentes | Cut seco (navegação é a transição) |
| Cursor em posição diferente | Cross dissolve 0.5s ou cut no momento de movimento do cursor |

#### Como Sincronizar Novamente

1. Reproduzir os últimos 5s da cena anterior
2. Reproduzir os primeiros 5s da cena regravada
3. Verificar que o cursor está em posição compatível
4. Verificar que o tom de voz é consistente
5. Ajustar o ponto de corte para minimizar a descontinuidade

---

## Checklist por Cena

### Cena 01 — Título
- [ ] Cursor parado no centro
- [ ] Tela de login carregada
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] Nenhum clique errado
- [ ] Movimentos suaves

### Cena 02 — Problema
- [ ] Cursor parado no centro
- [ ] Tela de login estável
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] Nenhum clique
- [ ] Movimentos suaves

### Cena 03 — Arquitetura
- [ ] Cursor parado no botão "Entrar" ao final
- [ ] Tela de login estável
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] Nenhum clique
- [ ] Movimentos suaves

### Cena 04 — Login
- [ ] Cursor parado no botão "Advogado" antes de clicar
- [ ] Campos preenchidos após clique
- [ ] Cursor parado no botão "Entrar" antes de clicar
- [ ] Dashboard carregado completamente
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] 2 cliques executados
- [ ] Movimentos suaves

### Cena 05 — Dashboard
- [ ] Dashboard carregado com documentos
- [ ] Cursor percorreu todos os 9 itens da navbar
- [ ] Cursor parou no nome/role do usuário
- [ ] Cursor parou no primeiro card
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] 1 clique (Upload PDF)
- [ ] Movimentos suaves pela navbar

### Cena 06 — Upload
- [ ] Campo de título preenchido
- [ ] Arquivo PDF selecionado
- [ ] Botão "Fazer Upload" clicado
- [ ] Loading aguardado completamente
- [ ] Tela de sucesso visível por 3s
- [ ] Dashboard com novo documento
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~60s)
- [ ] 3 cliques (campo, drop zone, botão)
- [ ] Cursor parado durante loading

### Cena 07 — Análise
- [ ] Documento selecionado no dropdown
- [ ] Loading aguardado completamente
- [ ] Card de resumo visível por 3s
- [ ] Scroll suave para grid 2x2
- [ ] Cada card de extração visitado
- [ ] Badges de risco apontados
- [ ] Cursor parado em "Iniciar Chat" ao final
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~90s)
- [ ] 2–3 cliques (navbar, dropdown se necessário)
- [ ] 1 scroll para baixo, 1 scroll para cima

### Cena 08 — Chat
- [ ] Conversa selecionada ou criada
- [ ] Pergunta digitada corretamente
- [ ] Botão Send clicado
- [ ] Resposta aguardada completamente
- [ ] Resposta estruturada visível por 3s
- [ ] Citações apontadas
- [ ] Disclaimer apontado
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~90s)
- [ ] 2 cliques (campo de texto, Send)
- [ ] Cursor parado durante loading

### Cena 09 — Riscos
- [ ] Documento selecionado
- [ ] Botão "Analyze Risks" clicado
- [ ] Loading aguardado completamente
- [ ] Overall risk card visível por 3s
- [ ] Risk card apontado
- [ ] Sources expandidas
- [ ] Disclaimer apontado
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~90s)
- [ ] 2–3 cliques (navbar/dropdown, Analyze Risks, Sources)
- [ ] 1 scroll para baixo

### Cena 10 — Automações
- [ ] Lista de automações carregada
- [ ] Status badge apontado
- [ ] Barra de progresso apontada
- [ ] Webhook status apontado
- [ ] Filtro e botão Atualizar apontados
- [ ] Links "Ver documento" e "Ver riscos" apontados
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] 1 clique (navbar)
- [ ] 1 scroll para baixo

### Cena 11 — Revisões
- [ ] Lista de análises carregada
- [ ] Filtros apontados (não clicados)
- [ ] Análise selecionada na lista
- [ ] Painel de detalhe aberto
- [ ] Histórico de revisões visível
- [ ] Botão "Aprovar" clicado
- [ ] Comentário digitado
- [ ] "Confirmar Revisão" clicado
- [ ] Histórico atualizado visível
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~60s)
- [ ] 4 cliques (card, Aprovar, comentário, Confirmar)
- [ ] 1 scroll para baixo

### Cena 12 — Métricas
- [ ] Dashboard de métricas carregado
- [ ] 4 cards superiores apontados individualmente
- [ ] Grid 2x2 visitado
- [ ] Estimativa de produtividade apontada
- [ ] Aviso (estimation_notice) apontado
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~45s)
- [ ] 1 clique (navbar)
- [ ] 2 scrolls para baixo

### Cena 13 — Comparação
- [ ] Documento A selecionado
- [ ] Documento B selecionado (diferente de A)
- [ ] Botão "Comparar Documentos" clicado
- [ ] Loading aguardado completamente
- [ ] Resultado visível por 3s
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~30s)
- [ ] 5 cliques (navbar, dropdown A, doc A, dropdown B, doc B, Comparar)
- [ ] Cursor parado durante loading

### Cena 14 — Encerramento
- [ ] Dashboard carregado e estático
- [ ] Cursor parado por longos períodos
- [ ] Movimentos mínimos e lentos
- [ ] Sem notificações
- [ ] Narração sincronizada
- [ ] Tempo correto (~60s)
- [ ] 1 clique (navbar Dashboard)
- [ ] Nenhum scroll
- [ ] Tela estática predominante

---

## Checklist Geral

### Antes da Gravação

- [ ] Backend rodando: `uvicorn app.main:app --reload`
- [ ] Frontend rodando: `npm run dev`
- [ ] Seed executado: `python -m app.seed`
- [ ] Demo check aprovado: `python -m scripts.demo_check`
- [ ] Pelo menos 2 documentos uploaded
- [ ] Pelo menos 1 conversa com mensagens
- [ ] Pelo menos 1 análise de riscos executada
- [ ] Pelo menos 1 automação completada
- [ ] Pelo menos 1 analysis record com revisão pendente
- [ ] Métricas populadas
- [ ] VITE_DEMO_MODE=true
- [ ] Navegador: Chrome, perfil limpo, zoom 100%, tema claro
- [ ] Barra de favoritos oculta
- [ ] Histórico e cache limpos
- [ ] Notificações desabilitadas
- [ ] "Não perturbe" ativado
- [ ] Monitor em 1920×1080, escala 100%
- [ ] Desktop limpo, papel de parede neutro
- [ ] Dock/Barra de tarefas em auto-ocultar
- [ ] OBS configurado: 1920×1080, 30fps, 6000 Kbps
- [ ] Microfone testado (narração em off)
- [ ] Roteiro de fala impresso ou em segundo monitor

### Durante a Gravação

- [ ] Seguir o shot list literalmente
- [ ] Cursor sempre visível e movendo suavemente
- [ ] Esperar carregamentos completamente
- [ ] Não clicar durante loading
- [ ] Não mover cursor durante loading
- [ ] Pausar 500ms antes de cada clique
- [ ] Pausar 500ms após cada clique
- [ ] Scroll suave e constante
- [ ] Nomear cada clipe: `cena_XX_nome.mp4`
- [ ] 3s de tela estática no início e fim de cada clipe

### Após a Gravação

- [ ] Todos os 14 clipes gravados
- [ ] Reproduzir cada clipe e verificar
- [ ] Áudio limpo (sem ruído, sem clique)
- [ ] Vídeo sem lag, drop frame ou artefato
- [ ] Nenhuma notificação apareceu
- [ ] Nenhuma informação pessoal visível
- [ ] Backup dos clipes para local secundário

### Antes da Edição

- [ ] Converter MKV para MP4 (sem re-encode)
- [ ] Ordenar clipes conforme timeline
- [ ] Consultar `10_VIDEO_EDITING_SCRIPT.md` para instruções de edição
- [ ] Verificar continuidade entre clipes
- [ ] Verificar sincronização de áudio

---

## Anexo — Tabela Resumo

| Cena | Tempo inicial | Tempo final | Página | Duração | Nº de cliques | Scroll | Tempo parado (aprox.) |
|------|---------------|-------------|--------|---------|---------------|--------|----------------------|
| 01 | 00:00:00 | 00:00:30 | Login | 30s | 0 | 0 | 20s |
| 02 | 00:00:30 | 00:01:15 | Login | 45s | 0 | 0 | 30s |
| 03 | 00:01:15 | 00:02:00 | Login | 45s | 0 | 0 | 28s |
| 04 | 00:02:00 | 00:02:30 | Login→Dashboard | 30s | 2 | 0 | 15s |
| 05 | 00:02:30 | 00:03:00 | Dashboard | 30s | 1 | 0 | 15s |
| 06 | 00:03:00 | 00:04:00 | Upload→Dashboard | 60s | 3 | 0 | 25s |
| 07 | 00:04:00 | 00:05:30 | Análise | 90s | 2–3 | 2 | 45s |
| 08 | 00:05:30 | 00:07:00 | Chat | 90s | 2 | 1 | 40s |
| 09 | 00:07:00 | 00:08:30 | Riscos | 90s | 3 | 1 | 45s |
| 10 | 00:08:30 | 00:09:15 | Automações | 45s | 1 | 1 | 25s |
| 11 | 00:09:15 | 00:10:15 | Revisões | 60s | 4 | 1 | 30s |
| 12 | 00:10:15 | 00:11:00 | Métricas | 45s | 1 | 2 | 25s |
| 13 | 00:11:00 | 00:11:30 | Comparação | 30s | 5 | 0 | 12s |
| 14 | 00:11:30 | 00:12:30 | Dashboard | 60s | 1 | 0 | 50s |
| **Total** | | | | **~12:30** | **25–27** | **8** | **~405s** |

---

## Validação

### Consistência com Documentação Existente

| Documento | Verificação | Status |
|-----------|-------------|--------|
| `02_DEMO_TIMELINE.md` | 14 cenas, mesmos tempos de início/término (00:00–12:30) | ✓ Consistente |
| `03_SCREEN_NAVIGATION_SCRIPT.md` | Mesmas URLs, botões, ações e resultados esperados | ✓ Consistente |
| `04_VIDEO_SPEECH_SCRIPT.md` | Marcações de fala e pausas alinhadas com ações do cursor | ✓ Consistente |
| `10_VIDEO_EDITING_SCRIPT.md` | Transições, cortes e tempos compatíveis | ✓ Consistente |

### Adaptação para Sem Webcam

As cenas 01–03 e 14 eram originalmente cenas de webcam nos documentos anteriores. Neste shot list, todas foram adaptadas para gravação de tela:

- **Cenas 01–03**: Tela de login visível com narração em off. Cursor move-se sobre os elementos da tela (logo, campos, credenciais demo) para ilustrar a narração.
- **Cena 14**: Dashboard visível com narração em off. Cursor parado em posições neutras, com movimentos mínimos para não distrair da narração de encerramento.

### Nenhuma Tela Inventada

Todas as URLs referenciadas existem em `App.tsx`:
- `/login`, `/dashboard`, `/upload`, `/chat`, `/analysis`, `/risks`, `/automations`, `/reviews`, `/insights`, `/comparison`

### Nenhuma Funcionalidade Inventada

Todos os botões, dropdowns, formulários e ações descritos existem no código frontend:
- Botão "Advogado" (credenciais demo) — `Login.tsx:86`
- Botão "Entrar" — `Login.tsx:76`
- Botão "Upload PDF" — `Dashboard.tsx:48`
- Campo "Título do Documento" — `Upload.tsx:62`
- Área de drop zone — `Upload.tsx:75`
- Botão "Fazer Upload" — `Upload.tsx:104`
- Dropdown de documentos — `Analysis.tsx:89`
- Botão "Iniciar Chat" — `Analysis.tsx:131`
- Botão "Analyze Risks" — `RiskAnalysis.tsx`
- Botão "Sources" — `RiskAnalysis.tsx`
- Campo de texto do chat — `Chat.tsx:235`
- Botão Send — `Chat.tsx:248`
- Botão "Aprovar" — `Reviews.tsx:349`
- Campo de comentário — `Reviews.tsx:377`
- Botão "Confirmar Revisão" — `Reviews.tsx:388`
- Dropdown "Documento A" — `Comparison.tsx:82`
- Dropdown "Documento B" — `Comparison.tsx:107`
- Botão "Comparar Documentos" — `Comparison.tsx:126`
- Navbar com 9 itens — `Layout.tsx:10`
