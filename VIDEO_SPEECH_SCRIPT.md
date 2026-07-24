# Script de Fala — Legal AI Copilot

**Duração estimada**: 7 a 9 minutos
**Idioma**: Português brasileiro
**Tom**: Profissional, técnico, direto, confiante

---

## [0:00 — Tela de título ou slide]

Olá, meu nome é Leonardo e este é o Legal AI Copilot, um MVP que construí para acelerar a análise de contratos jurídicos usando inteligência artificial.

O problema é simples: escritórios de advocacia gastam horas revisando contratos manualmente para identificar riscos, extrair informações e comparar documentos. É um trabalho repetitivo que consome tempo que poderia ser dedicado a análise estratégica.

O objetivo deste MVP é demonstrar que é possível acelerar esse processo com IA, mantendo o profissional jurídico no controle total através de uma camada de revisão humana obrigatória.

## [1:10 — Mostrar diagrama de arquitetura]

A arquitetura é dividida em frontend em React com TypeScript e backend em FastAPI com Python. O banco de dados é SQLite para o MVP, com caminho de migração para PostgreSQL.

O componente central é o Agent Router, que é determinístico — ele classifica a intenção do usuário por palavras-chave, sem chamar o LLM. Isso significa zero custo de tokens para roteamento e resposta instantânea.

Para as operações que precisam de IA — resumo, extração, comparação e perguntas e respostas — uso o GPT-4o da OpenAI via LangChain. A análise de riscos é um caso à parte: é totalmente heurística, baseada em palavras-chave, sem LLM. Vou mostrar isso em detalhe mais adiante.

## [2:00 — Abrir o navegador em http://localhost:5173]

[mostrar tela de login]

Aqui na tela de login, tenho autenticação JWT com cinco papéis: ADMIN, LAWYER, ASSISTANT, CLIENT e VIEWER. As credenciais de demonstração só aparecem em modo de desenvolvimento por segurança.

Vou entrar como advogado.

[ clicar em "Advogado" e depois "Entrar" ]

## [2:40 — Tela de Dashboard]

[mostrar dashboard]

Agora vou fazer o upload de um contrato.

[abrir documento]

[clicar em "Upload", preencher título, selecionar PDF, clicar "Fazer Upload"]

O upload dispara uma automação em background que executa automaticamente o resumo e a análise de riscos. Vou mostrar isso na aba de automações.

[mostrar automação]

Aqui dá para ver o AutomationRun com o progresso, o step atual e o status. Quando configurado, o sistema também envia um webhook compatível com n8n ao final da análise. O workflow de exemplo do n8n está incluído no repositório.

## [3:30 — Abrir Chat]

[mostrar chat]

Agora vou demonstrar o chat com RAG. Vou selecioncionar o documento e fazer uma pergunta.

[selecionar documento, digitar "qual é o valor do contrato?"]

O Agent Router identificou a intenção de pergunta e direcionou para a ferramenta de busca semântica. O sistema gerou um embedding da minha pergunta, comparou com os embeddings dos chunks do documento por similaridade cosseno, e enviou os trechos mais relevantes como contexto para o GPT-4o.

A resposta vem com citações estruturadas, mostrando exatamente de qual parte do documento a informação foi extraída, com número de página e trecho. E aqui embaixo, o confidence score — uma pontuação de 0 a 100 que indica o nível de sustentação documental da resposta.

## [4:20 — Abrir página de Riscos]

[mostrar riscos]

Agora a análise de riscos. Esta parte é diferente — não usa LLM. É uma análise heurística determinística, baseada em palavras-chave.

[selecionar documento]

O sistema verifica se o contrato contém cláusulas de confidencialidade, conformidade com LGPD, e rescisão. Também detecta padrões problemáticos como multa ilimitada, renovação automática e pagamento indefinido.

Aqui no resultado, posso ver o risco geral, a lista de riscos identificados com severidade e categoria, e as recomendações. O confidence score aqui é calculado por uma fórmula própria, não pelo AIValidator.

E sempre tem o disclaimer jurídico embaixo — "esta análise não substitui a revisão de um profissional jurídico especializado."

## [5:10 — Voltar ao Chat]

[mostrar chat]

Para demonstrar os guardrails, vou fazer uma pergunta sobre algo que não está no contrato.

[digitar "qual a taxa de juros?"]

Veja — a resposta foi bloqueada. O AIValidator calculou o confidence score e, como não encontrou evidências suficientes no documento, bloqueou a resposta. O usuário não vê uma alucinação — vê uma mensagem clara de que não há evidências suficientes.

O threshold de bloqueio é configurável, padrão em 60 pontos. Abaixo disso, a resposta é bloqueada.

## [6:00 — Abrir Revisões]

[mostrar revisão]

Toda análise gerada pelo sistema — seja via chat, endpoint direto ou automação — é persistida como um AnalysisRecord e pode ser revisada por um humano.

Aqui vejo a lista de análises com filtros por tipo e status. Vou abrir uma para revisar.

[clicar em uma análise]

Posso ver o conteúdo, o structured data, o confidence score, as citações e o disclaimer. Agora vou aprovar esta análise.

[mover para PENDING_REVIEW se necessário, clicar "Aprovar", escrever comentário]

E aqui está o histórico de revisão — é append-only, ou seja, nunca é modificado ou deletado. Cada revisão fica registrada com quem revisou, quando, e a decisão.

## [6:50 — Abrir Métricas]

[mostrar métricas]

O dashboard de métricas mostra estimativas de produtividade — tempo manual estimado versus tempo economizado com IA.

É importante destacar: estes são estimativas do MVP, baseadas em tempos manuais configuráveis, não resultados medidos em produção. Os valores são ajustáveis via variáveis de ambiente.

Aqui também vejo análises por tipo, riscos por severidade, e o status das automações.

## [7:30 — Fazer logout]

Em termos de segurança: senhas com Argon2, JWT com expiração, RBAC em todos os endpoints, e cada usuário só acessa seus próprios documentos e análises — exceto o ADMIN, que tem visão global.

Sobre limitações: o sistema não tem OCR, usa SQLite sem fila de tarefas externa, e o refresh token não é renovado automaticamente. O AIValidator está integrado apenas em Q&A, não nas outras operações com LLM.

Como próximos passos, migraria para PostgreSQL com Celery, integraria o AIValidator em todas as operações, adicionaria RAG semântico na análise de riscos, e calibraria as métricas com dados reais.

## [8:10 — Mostrar GitHub]

O projeto tem 166 testes aprovados, zero falhas, migrations validadas e frontend compilando. O código está disponível no GitHub.

Obrigado.
