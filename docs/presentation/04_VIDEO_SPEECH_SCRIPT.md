# Roteiro de Fala — Legal AI Copilot

> Script sincronizado com as cenas. Linguagem técnica, natural e profissional.
> Sem linguagem de marketing. Sem promessas infladas.

---

## Cena 01 — Abertura (00:00–00:30)

> [PAUSA 2s — tela estática]

Este é o Legal AI Copilot, um MVP de inteligência artificial para análise de contratos jurídicos. O sistema oferece resumo automático, extração de informações estruturadas, análise de riscos, chat com roteamento de agente, revisão humana e métricas de impacto.

> [PAUSA 1s]

Nesta demonstração, vou percorrer cada funcionalidade do sistema, mostrando como ele funciona na prática e quais são suas limitações.

---

## Cena 02 — Problema e Contexto (00:30–01:15)

A análise manual de contratos é um processo demorado, repetitivo e sujeito a erros. Advogados precisam ler documentos extensos, identificar cláusulas críticas, verificar riscos e produzir resumos — tarefas que consomem horas e carecem de rastreabilidade.

> [PAUSA 1s]

O Legal AI Copilot aborda esse problema automatizando quatro tarefas principais: resumo de documentos, extração estruturada de informações, comparação entre contratos e análise de riscos. Cada análise passa por guardrails com validação de confiança e citações obrigatórias, e por revisão humana antes de ser considerada final.

---

## Cena 03 — Arquitetura (01:15–02:00)

A stack do projeto inclui FastAPI no backend com Python 3.12, React com TypeScript no frontend, SQLAlchemy como ORM e SQLite como banco de dados para o MVP.

> [PAUSA 1s]

A autenticação usa JWT com access e refresh tokens, e o controle de acesso é baseado em papéis — RBAC — com cinco níveis: admin, lawyer, assistant, client e viewer.

> [PAUSA 1s]

O agent router é determinístico, classificando a intenção do usuário por palavras-chave. Os guardrails validam confiança, exigem citações e incluem disclaimer jurídico. A análise de riscos é heurística, baseada em palavras-chave, e funciona sem necessidade de API key da OpenAI.

---

## Cena 04 — Login (02:00–02:30)

> [TRANSIÇÃO para http://localhost:5173/login]

A tela de login oferece dois perfis de demonstração: advogado e administrador.

> [CLICAR no botão "Advogado" — credenciais preenchem automaticamente]

Vou usar o perfil de advogado para esta demonstração.

> [CLICAR "Entrar" — aguardar redirect]

O sistema autentica com JWT e redireciona para o dashboard. O RBAC controla quais dados e ações estão disponíveis para cada papel.

---

## Cena 05 — Dashboard (02:30–03:00)

> [TELA: Dashboard]

O dashboard lista todos os documentos do usuário. Cada card mostra o título, nome do arquivo, número de páginas, status de processamento e data de criação.

> [APONTAR a barra de navegação]

A barra de navegação superior dá acesso a nove funcionalidades: dashboard, upload, chat, análise, riscos, automações, revisões, métricas e comparação.

> [APONTAR nome do usuário e role no canto direito]

No canto direito, vemos o nome do usuário e seu papel, com opção de logout. Usuários não-admin veem apenas seus próprios documentos.

---

## Cena 06 — Upload de Contrato (03:00–04:00)

> [CLICAR "Upload PDF" — navegar para /upload]

Vou fazer o upload de um contrato de prestação de serviços.

> [DIGITAR título: "Contrato de Prestação de Serviços — Demo"]

> [CLICAR na área de upload e selecionar o PDF]

> [CLICAR "Fazer Upload"]

O processamento extrai o texto do PDF, divide em chunks e gera embeddings se a API key da OpenAI estiver configurada. Em paralelo, uma automação é disparada em background para gerar resumo, análise de riscos e enviar webhook.

> [AGUARDAR tela de sucesso e redirect]

Upload concluído. O documento já aparece no dashboard com status "Pronto".

---

## Cena 07 — Análise — Resumo e Extração (04:00–05:30)

> [CLICAR "Análise" na navbar]

> [SELECIONAR documento no dropdown se necessário]

A página de análise gera um resumo do contrato e extrai informações estruturadas.

> [APONTAR o card de resumo]

O resumo é gerado automaticamente a partir do texto extraído.

> [ROLAR para baixo — mostrar grid 2x2]

Abaixo, temos quatro cards de extração: partes envolvidas, datas importantes, valores monetários e cláusulas críticas.

> [APONTAR Partes Envolvidas]

As partes identificadas incluem contratante e contratada, com seus respectivos dados.

> [APONTAR Datas Importantes]

As datas extraídas incluem vigência, assinatura e eventuais prazos.

> [APONTAR Valores]

Os valores monetários são identificados com tipo e descrição.

> [APONTAR Cláusulas Importantes]

Cada cláusula tem um badge de risco — baixo, médio ou alto — baseado na análise heurística. Cada análise gerada é persistida como registro para revisão humana posterior.

---

## Cena 08 — Chat com Agent Router (05:30–07:00)

> [CLICAR "Iniciar Chat" ou navegar para /chat]

O chat permite interagir com o documento usando linguagem natural.

> [APONTAR a sidebar com lista de conversas]

A barra lateral mostra conversas existentes e permite criar novas.

> [DIGITAR: "Quais são os riscos deste contrato?"]

> [CLICAR Send — aguardar resposta]

O agent router classifica a intenção da pergunta — neste caso, identificação de riscos — e executa a ferramenta apropriada.

> [APONTAR a resposta estruturada com riscos]

A resposta inclui riscos identificados com severidade, descrição e recomendação.

> [APONTAR as citações abaixo da resposta]

Cada resposta inclui citações do documento original, com número de página e trecho relevante.

> [APONTAR o disclaimer ao final]

E um disclaimer jurídico, indicando que a análise não substitui revisão profissional. Os guardrails verificam nível de confiança, exigem citações mínimas e bloqueiam respostas abaixo do threshold.

---

## Cena 09 — Análise de Riscos (07:00–08:30)

> [CLICAR "Riscos" na navbar]

> [SELECIONAR documento se necessário]

A página de análise de riscos oferece uma visão dedicada dos riscos contratuais.

> [CLICAR "Analyze Risks" — aguardar resultado]

> [APONTAR o card de Overall Risk]

O resultado mostra um risco geral — baixo, médio, alto ou crítico — com pontuação de confiança e nível.

> [APONTAR os risk cards]

Cada risco identificado tem severidade, categoria, descrição e recomendação. As categorias incluem confidencialidade, LGPD, rescisão, pagamento, responsabilidade, multas, foro, SLA, propriedade intelectual, renovação e duração.

> [CLICAR "Sources" em um risk card]

As citações mostram o trecho exato do documento que motivou a identificação do risco, com número de página e score de similaridade.

> [APONTAR o disclaimer]

É importante destacar que esta análise é heurística, baseada em palavras-chave, e não utiliza LLM. O score de similaridade é fixo em 0.7. Isso é uma limitação consciente do MVP.

---

## Cena 10 — Automações (08:30–09:15)

> [CLICAR "Automações" na navbar]

Cada upload dispara uma automação em background com múltiplas etapas: processamento do documento, geração de resumo, análise de riscos e envio de webhook para integração com n8n.

> [APONTAR os cards de automação]

Cada run mostra o status — pendente, executando, concluído, falhou ou sucesso parcial — o step atual, uma barra de progresso e o status do webhook.

> [APONTAR o filtro de status]

É possível filtrar por status. Runs com falha ou sucesso parcial podem ser retentados com o botão "Tentar Novamente".

> [APONTAR os links "Ver documento" e "Ver riscos"]

Cada run tem links diretos para o documento e para a análise de riscos associada.

---

## Cena 11 — Revisão Humana (09:15–10:15)

> [CLICAR "Revisões" na navbar]

A revisão humana é o controle de qualidade do sistema. Toda análise gerada pela IA passa por revisão antes de ser considerada final.

> [APONTAR a lista de análises à esquerda]

A lista mostra cada análise com tipo, status, nível de confiança, risco geral e versão. É possível filtrar por tipo e por status.

> [CLICAR em uma análise para abrir o detalhe]

O painel de detalhe mostra o conteúdo da análise, resultados estruturados, o disclaimer e o histórico de revisões.

> [APONTAR o histórico]

O histórico é append-only — cada revisão é adicionada sem sobrescrever as anteriores, garantindo trilha de auditoria completa.

> [CLICAR "Aprovar" e digitar comentário]

> [CLICAR "Confirmar Revisão"]

A state machine controla o fluxo: uma análise começa como gerada, passa para pendente de revisão, e pode ser aprovada, rejeitada ou marcada como correções necessárias. Apenas papéis de admin e advogado podem revisar.

---

## Cena 12 — Métricas de Impacto (10:15–11:00)

> [CLICAR "Métricas" na navbar]

O dashboard de métricas agrega dados de produtividade do sistema.

> [APONTAR os 4 cards superiores]

Os cards superiores mostram total de documentos, análises geradas, tempo poupado em horas e taxa de aprovação.

> [APONTAR o grid 2x2]

Abaixo, quatro visualizações: análises por tipo, status das revisões, riscos por severidade e automações por status.

> [APONTAR a estimativa de produtividade]

A estimativa de produtividade compara tempo manual estimado versus tempo poupado pela IA. É importante notar que estas são estimativas do MVP, não calibradas com dados reais de produção. O aviso no rodapé deixa isso explícito.

> [APONTAR o aviso]

Administradores veem métricas globais; outros usuários veem apenas suas próprias métricas.

---

## Cena 13 — Comparação de Contratos (11:00–11:30)

> [CLICAR "Comparação" na navbar]

A comparação permite analisar dois contratos lado a lado.

> [SELECIONAR Documento A no dropdown]

> [SELECIONAR Documento B no dropdown]

> [CLICAR "Comparar Documentos" — aguardar resultado]

O resultado destaca semelhanças e diferenças entre os dois documentos. Esta funcionalidade requer pelo menos dois documentos no sistema.

---

## Cena 14 — Encerramento (11:30–12:30)

> [TRANSIÇÃO para webcam ou tela estática]

Para concluir, é importante ser transparente sobre as limitações do MVP.

> [PAUSA 1s]

A análise de riscos é heurística, baseada em palavras-chave, sem uso de LLM ou RAG semântico. O score de similaridade das citações é fixo em 0.7. Não há OCR — apenas extração de texto de PDFs. O banco de dados é SQLite, adequado para MVP mas não para produção. As métricas de produtividade são estimativas, não calibradas. E não há auto-refresh do token JWT — em caso de expiração, o usuário é redirecionado para login.

> [PAUSA 1s]

O sistema funciona em modo heurístico sem necessidade de API key da OpenAI, o que facilita demonstrações e desenvolvimento local. Com a API key configurada, embeddings e análise via LLM podem ser ativados.

> [PAUSA 1s]

O Legal AI Copilot demonstra um fluxo completo: upload, processamento, análise, chat, riscos, automação, revisão humana e métricas — com guardrails, RBAC e rastreabilidade.

> [PAUSA 2s — fade out]

---

## Notas de Estilo

- **Tom**: Técnico, natural, direto. Sem entusiasmo exagerado.
- **Velocidade**: Pausa de 1 segundo entre frases longas. Pausa de 2 segundos entre tópicos.
- **Evitar**: "Inovador", "revolucionário", "cutting-edge", "game-changer", qualquer termo de marketing.
- **Usar**: "MVP", "heurística", "determinístico", "guardrails", "RBAC", "state machine", "append-only".
- **Honestidade**: Mencionar limitações no momento em que são relevantes, não apenas no encerramento.
