# Roteiro de Apresentação em Vídeo — Legal AI Copilot MVP

**Apresentador:** Leonardo Fragoso  
**Duração obrigatória:** 5 a 10 minutos (alvo: 7-9 minutos)  
**Data de preparação:** 26 de julho de 2026  
**Status:** Pronto para gravação

---

## 1. Resumo Executivo da Apresentação

### Nome da Solução
**Legal AI Copilot**

### Descrição em Uma Frase
Plataforma de análise inteligente de documentos jurídicos que combina IA generativa com recuperação semântica para transformar contratos extensos em informações estruturadas, rastreáveis e revisáveis por profissionais jurídicos.

### Problema Resolvido
Advogados e equipes jurídicas gastam horas lendo contratos extensos, extraindo informações-chave, identificando riscos e comparando cláusulas. Este trabalho é repetitivo, propenso a erros e consome tempo que poderia ser dedicado à análise estratégica.

### Público-Alvo
- Advogados e consultores jurídicos
- Equipes de legal operations
- Departamentos jurídicos corporativos

### Principal Diferencial
A solução não apenas gera respostas com IA — ela **recupera trechos específicos dos documentos**, **estrutura as respostas em JSON**, **rastreia as fontes**, **calcula um score de confiança** baseado em evidências reais, e **bloqueia respostas sem sustentação documental**. Tudo isso mantém o profissional jurídico no controle da decisão final.

### Funcionalidades Demonstradas
1. Upload de contrato PDF
2. Extração automática de texto e chunking
3. Geração de embeddings e busca semântica
4. Chat com RAG (Retrieval-Augmented Generation)
5. Resumo automático do contrato
6. Extração estruturada de informações (partes, datas, valores, cláusulas)
7. Comparação entre dois contratos
8. Análise de riscos com identificação de cláusulas problemáticas
9. Revisão humana com aprovação/rejeição
10. Métricas de impacto (tempo economizado)

### Duração Estimada
7 a 9 minutos

---

## 2. Preparação Antes da Gravação

### Checklist de Serviços

#### Backend
- [ ] Python 3.12+ instalado
- [ ] Virtual environment criado e ativado
- [ ] Dependências instaladas: `pip install -r requirements.txt`
- [ ] Banco de dados inicializado: `alembic upgrade head`
- [ ] Usuários demo criados: `ENVIRONMENT=development python -m app.seed`
- [ ] OPENAI_API_KEY configurada no `.env`
- [ ] Backend iniciado: `uvicorn app.main:app --reload`
- [ ] Backend respondendo em `http://localhost:8000`

#### Frontend
- [ ] Node.js 18+ instalado
- [ ] npm install executado
- [ ] `.env` configurado com `VITE_API_URL=http://localhost:8000`
- [ ] Frontend iniciado: `npm run dev`
- [ ] Frontend acessível em `http://localhost:5173`

#### Dados de Demonstração
- [ ] Arquivo de contrato disponível: `Contrato_Prestacao_Servicos_Teste.pdf`
- [ ] Segundo contrato para comparação: `contrato.pdf`
- [ ] Credenciais demo memorizadas:
  - **LAWYER**: `lawyer@demo.com` / `demo123456`
  - **ADMIN**: `admin@demo.com` / `admin123456`

### Verificações Pré-Gravação

```bash
# Backend funcional
cd backend && source venv/bin/activate
python -m pytest tests/test_demo_smoke.py -v
# Esperado: 166 testes passando

# Health check
curl http://localhost:8000/health

# Frontend carregando
# Abrir http://localhost:5173 no navegador
```

### Cuidados Críticos

- ❌ **NÃO mostrar a OPENAI_API_KEY na tela**
- ❌ **NÃO mostrar tokens JWT completos**
- ❌ **NÃO usar dados jurídicos reais ou confidenciais**
- ✅ Usar apenas os arquivos de demonstração fornecidos

### Plano Alternativo para Falhas

#### Se o OpenAI API falhar
- O sistema continuará funcionando em modo heurístico
- Demonstrar a análise de riscos (determinística, sem LLM)

#### Se o upload falhar
- Usar um documento previamente carregado

#### Se o frontend não carregar
- Usar a API diretamente via Swagger (`http://localhost:8000/docs`)

---

## 3. Roteiro Cronológico com Marcação de Tempo

### **00:00–00:45 — Apresentação e Contexto**

**Tempo**: 45 segundos

**Tela**: Apresentador em câmera ou slide com nome da solução

**Fala**:
"Olá, meu nome é Leonardo Fragoso. Neste vídeo vou apresentar o Legal AI Copilot, uma solução que desenvolvi para automatizar a análise de documentos jurídicos utilizando Inteligência Artificial generativa, recuperação semântica e prompts estruturados.

O projeto nasceu de um problema real: advogados e equipes jurídicas gastam horas lendo contratos extensos, extraindo informações-chave, identificando riscos e comparando cláusulas. Este trabalho é repetitivo, propenso a erros e consome tempo que poderia ser dedicado à análise estratégica.

Nesta demonstração, vou mostrar como a solução transforma um contrato em informações estruturadas, rastreáveis e revisáveis, mantendo sempre o profissional jurídico no controle da decisão final."

**Competência**: Visão de produto, compreensão do problema, comunicação clara

---

### **00:45–01:30 — Problema, Objetivo e Stack**

**Tempo**: 45 segundos

**Tela**: Slide ou diagrama da arquitetura

**Fala**:
"O desafio é transformar documentos jurídicos extensos em informações estruturadas sem perder a rastreabilidade. A solução combina três pilares:

Primeiro, **Recuperação Semântica**: quando um usuário faz uma pergunta, o sistema não processa o documento inteiro. Ele recupera apenas os trechos mais relevantes usando embeddings e similaridade de cosseno.

Segundo, **IA Generativa Estruturada**: o modelo GPT-4 recebe o contexto recuperado e gera respostas em formato estruturado — JSON com partes, datas, valores e cláusulas.

Terceiro, **Guardrails e Revisão Humana**: a resposta é validada contra as fontes. Se não houver evidência suficiente, o sistema bloqueia a resposta. Todas as análises são persistidas e podem ser aprovadas ou rejeitadas por um profissional jurídico.

A stack é Python com FastAPI no backend, React no frontend, SQLite para persistência, e OpenAI para o modelo de linguagem."

**Competência**: Arquitetura de sistemas, domínio de IA generativa

---

### **01:30–02:15 — Arquitetura Técnica**

**Tempo**: 45 segundos

**Tela**: Diagrama de arquitetura ou Swagger API Docs

**Fala**:
"A arquitetura segue um padrão clássico com camadas bem definidas. No frontend, temos uma interface React que permite fazer login, enviar documentos e interagir com o sistema.

No backend, a API FastAPI orquestra todo o fluxo. Quando um contrato é enviado, o sistema extrai o texto, divide em chunks com sobreposição, e gera embeddings — representações vetoriais que capturam o significado semântico.

Esses embeddings são armazenados no SQLite junto com os chunks. Quando uma pergunta chega, o sistema recupera os chunks mais similares usando cálculo de similaridade de cosseno.

O contexto recuperado é enviado ao modelo GPT-4 junto com um prompt estruturado. O modelo gera a resposta, que passa por validação de confiança antes de ser retornada.

Todas as análises são persistidas com histórico completo, permitindo revisão humana e rastreabilidade."

**Competência**: Design de arquitetura, integração de sistemas, conhecimento de RAG

---

### **02:15–05:30 — Demonstração Funcional Completa (3 min 15 seg)**

#### **2.1 — Login e Dashboard (02:15–02:45)**

**Tempo**: 30 segundos

**Tela**: Frontend em `http://localhost:5173`, tela de login

**Ações**:
1. Abrir o navegador com o frontend
2. Preencher email: `lawyer@demo.com`
3. Preencher senha: `demo123456`
4. Clicar em "Entrar"
5. Mostrar o dashboard

**Fala**:
"Vou começar fazendo login na plataforma com as credenciais de demonstração. Após autenticação, o advogado acessa o dashboard onde pode ver todos os seus documentos e iniciar análises. A autenticação é baseada em JWT com tokens que expiram em 30 minutos, e o sistema implementa controle de acesso por papéis."

**Competência**: Segurança (autenticação JWT, RBAC), UX

---

#### **2.2 — Upload de Contrato (02:45–03:15)**

**Tempo**: 30 segundos

**Tela**: Dashboard com botão de upload, diálogo de seleção de arquivo

**Ações**:
1. Clicar no botão "Enviar Contrato"
2. Selecionar `Contrato_Prestacao_Servicos_Teste.pdf`
3. Preencher título: "Contrato de Prestação de Serviços"
4. Clicar em "Enviar"
5. Aguardar processamento (2-3 segundos)
6. Mostrar o documento na lista

**Fala**:
"Vou fazer upload de um contrato de prestação de serviços. O sistema extrai o texto automaticamente, divide em chunks inteligentes com sobreposição, e gera embeddings para cada chunk. Tudo isso acontece de forma assíncrona, então o usuário não fica esperando."

**Competência**: Processamento de documentos, automação assíncrona

---

#### **2.3 — Chat com RAG (03:15–04:15)**

**Tempo**: 1 minuto

**Tela**: Interface de chat com pergunta e resposta

**Ações**:
1. Clicar na aba "Chat"
2. Digitar: "Qual é o valor total do contrato?"
3. Enviar a pergunta
4. Aguardar a resposta (3-5 segundos)
5. Mostrar a resposta com score de confiança e citações

**Fala**:
"Quando envio a pergunta, o sistema gera um embedding da pergunta, compara com todos os chunks usando similaridade de cosseno, recupera os trechos mais relevantes, e envia ao modelo GPT-4 junto com um prompt estruturado.

O modelo gera a resposta, que passa por validação. O sistema verifica se existem chunks recuperados, se a resposta cita as fontes, se o score de similaridade é adequado, e se a confiança é suficiente.

A resposta é retornada com um score de confiança — neste caso, 85 pontos, o que significa alta sustentação documental. As citações mostram exatamente de qual trecho do documento a resposta foi extraída. Isso é crucial em contexto jurídico."

**Competência**: RAG, engenharia de prompts, guardrails, rastreabilidade

---

#### **2.4 — Análise de Riscos (04:15–04:50)**

**Tempo**: 35 segundos

**Tela**: Página de análise de riscos com lista de riscos

**Ações**:
1. Clicar na aba "Análise de Riscos"
2. Clicar em "Analisar Riscos"
3. Aguardar análise (2-3 segundos)
4. Mostrar a lista de riscos identificados

**Fala**:
"A análise de riscos identifica cláusulas problemáticas usando um mecanismo determinístico baseado em palavras-chave. Neste contrato, o sistema identificou cinco riscos: multa ilimitada (crítico), falta de cláusula de confidencialidade (médio), falta de conformidade LGPD (alto), renovação automática (médio), e pagamento indefinido (alto).

Cada risco vem com uma recomendação de ação. Este mecanismo é determinístico — não depende de LLM — então é rápido e previsível. Mas é importante notar que é uma primeira camada de análise. O profissional jurídico sempre revisa e valida os riscos identificados."

**Competência**: Análise heurística, categorização de riscos

---

#### **2.5 — Extração Estruturada (04:50–05:15)**

**Tempo**: 25 segundos

**Tela**: Página de extração com dados estruturados em JSON ou tabela

**Ações**:
1. Clicar na aba "Extração"
2. Clicar em "Extrair Informações"
3. Aguardar extração (3-5 segundos)
4. Mostrar os dados estruturados

**Fala**:
"A extração estruturada transforma o texto livre do contrato em dados estruturados — JSON com campos bem definidos. O sistema identifica partes (quem contrata quem), datas (início, término, renovação), valores (salários, custos, multas), e cláusulas principais.

Isso permite que o profissional jurídico veja rapidamente os termos-chave sem precisar ler o contrato inteiro. E porque os dados são estruturados, podem ser exportados ou integrados com outros sistemas."

**Competência**: Processamento de linguagem natural, estruturação de dados

---

#### **2.6 — Comparação de Contratos (05:15–05:30)**

**Tempo**: 15 segundos

**Tela**: Página de comparação com resultado

**Ações**:
1. Clicar na aba "Comparação"
2. Selecionar dois contratos
3. Clicar em "Comparar"
4. Mostrar as diferenças principais

**Fala**:
"Quando um profissional jurídico precisa comparar duas versões de um contrato, o sistema automatiza essa tarefa. Ele identifica as similaridades, as diferenças e gera um resumo executivo. Isso economiza tempo significativo em negociações."

**Competência**: Análise comparativa, automação

---

### **05:30–06:30 — LLM, Engenharia de Prompts e Guardrails (1 min)**

**Tempo**: 1 minuto

**Tela**: Código do prompt ou slide com fórmula de confiança

**Fala**:
"Vou mostrar como a engenharia de prompts funciona. [Mostrar o prompt no código]

O prompt tem várias seções: Definição de Papel, Regras Importantes, e Formato de Resposta. Engenharia de prompts não é apenas escrever uma pergunta — é criar um contrato de comportamento com o modelo.

Além do prompt, o sistema implementa guardrails — validações determinísticas que bloqueiam respostas sem evidência suficiente.

O score de confiança é calculado assim:
- **Fontes** (até 30 pontos): Quantos chunks foram recuperados?
- **Similaridade** (até 30 pontos): Qual é o score médio de similaridade?
- **Citações** (até 20 pontos): Quantas citações foram extraídas?
- **Consistência** (até 10 pontos): A resposta é consistente com as fontes?
- **Qualidade** (até 10 pontos): Os chunks recuperados têm conteúdo significativo?

Se o score cair abaixo de 60 pontos, a resposta é bloqueada. Melhor dizer 'não sei' do que inventar uma resposta que pode ter consequências legais."

**Competência**: Engenharia de prompts, design de guardrails

---

### **06:30–07:30 — RAG, Embeddings e Busca Semântica (1 min)**

**Tempo**: 1 minuto

**Tela**: Diagrama de RAG ou código do serviço de embeddings

**Fala**:
"RAG — Retrieval-Augmented Generation — é o coração desta solução. Quando um contrato é enviado, o sistema extrai o texto, divide em chunks de 1000 caracteres com 20% de sobreposição, e gera embeddings usando o modelo text-embedding-3-small da OpenAI.

Cada chunk vira um vetor de 1536 dimensões que captura seu significado semântico. Quando uma pergunta chega, o sistema gera embedding da pergunta, calcula similaridade de cosseno com todos os embeddings dos chunks, recupera os top-5 chunks mais similares, e envia o contexto ao modelo GPT-4.

Por que isso funciona? Porque o embedding captura significado semântico. Uma pergunta como 'Qual é o custo?' será similar a um chunk que diz 'O valor total é R$ 50.000'. Não é busca por palavras-chave — é busca por significado.

Neste MVP, usamos SQLite com cálculo de similaridade em memória. Para produção, eu implementaria pgvector, Qdrant, busca híbrida, e reranking. Isso aumentaria a precisão e a escalabilidade."

**Competência**: Conhecimento profundo de RAG, embeddings, escalabilidade

---

### **07:30–08:15 — Revisão Humana, Monitoramento e Segurança (45 seg)**

**Tempo**: 45 segundos

**Tela**: Página de revisões com formulário de aprovação/rejeição

**Fala**:
"Uma característica crítica desta solução é a revisão humana obrigatória. Nenhuma análise gerada pela IA é considerada final sem aprovação de um profissional jurídico.

Todas as análises são persistidas em um banco de dados com histórico completo. Um advogado pode aprovar, rejeitar, ou solicitar mudanças. Cada decisão é registrada com timestamp, nome do revisor e comentário. Isso cria uma trilha de auditoria completa.

Em termos de segurança: autenticação JWT, RBAC, ownership enforcement, sem dados sensíveis em logs, senhas com hash Argon2.

Para uma implantação real em um escritório de advocacia, eu adicionaria: LGPD compliance, criptografia em repouso, criptografia em trânsito, segregação de dados por cliente, auditoria detalhada, validação de arquivos, contrato com OpenAI, e revisão jurídica."

**Competência**: Segurança, conformidade, responsabilidade jurídica

---

### **08:15–09:00 — Resultados, Impacto e Conclusão (45 seg)**

**Tempo**: 45 segundos

**Tela**: Página de métricas de impacto ou slide com números

**Fala**:
"O sistema estima o tempo economizado em cada análise. Para um resumo, o tempo manual estimado é 30 minutos. Com a automação, 2-3 segundos. Para uma extração, 45 minutos manualmente, 3-5 segundos com automação. Para uma comparação, 90 minutos manualmente, 5-10 segundos com automação.

Isso não significa que o profissional economiza 30 minutos por resumo — ele ainda precisa revisar e validar. Mas a automação reduz o trabalho repetitivo, permitindo que ele dedique tempo à análise estratégica.

Este é um MVP — uma prova de conceito. Algumas funcionalidades ainda podem evoluir. Mas a arquitetura foi projetada para evoluir. Cada componente é modular e pode ser substituído ou melhorado sem afetar o resto do sistema.

Com este projeto, procurei demonstrar não apenas uma integração com um modelo de linguagem, mas a construção de um fluxo completo — desde o processamento dos documentos até a entrega de uma resposta contextualizada, rastreável e revisável.

A solução ainda pode evoluir em observabilidade, segurança e avaliação contínua. Mas o MVP valida a arquitetura e mostra como a IA pode reduzir atividades repetitivas sem retirar do profissional jurídico a responsabilidade pela decisão final.

Obrigado."

**Competência**: Pensamento crítico, honestidade sobre limitações, visão de futuro

---

## 4. Mapa Visual da Gravação

| Tempo | Tela | Ação | Fala Principal | Competência | Plano Alternativo |
|-------|------|------|---|---|---|
| 00:00–00:45 | Apresentação | Apresentar-se | "Olá, meu nome é Leonardo..." | Visão de produto | N/A |
| 00:45–01:30 | Slide/Arquitetura | Descrever problema | "O desafio é transformar..." | Arquitetura | Mostrar diagrama |
| 01:30–02:15 | API Docs | Explicar fluxo | "A arquitetura segue..." | Design | Usar Swagger |
| 02:15–02:45 | Frontend Login | Fazer login | "Vou fazer login..." | Segurança | Usar API |
| 02:45–03:15 | Dashboard | Upload | "Vou fazer upload..." | Automação | Documento pré-carregado |
| 03:15–04:15 | Chat | Pergunta e resposta | "Quando envio a pergunta..." | RAG, guardrails | Resultado pré-gravado |
| 04:15–04:50 | Análise Riscos | Executar análise | "A análise de riscos..." | Análise heurística | Resultado em slide |
| 04:50–05:15 | Extração | Executar extração | "A extração estruturada..." | NLP | JSON em slide |
| 05:15–05:30 | Comparação | Comparar contratos | "Quando um profissional..." | Automação | Resultado em slide |
| 05:30–06:30 | Código/Slide | Mostrar prompt | "Vou mostrar como..." | Engenharia de prompts | Documentação |
| 06:30–07:30 | Diagrama | Explicar RAG | "RAG é o coração..." | RAG, embeddings | Diagrama em slide |
| 07:30–08:15 | Revisões | Mostrar revisão | "Uma característica crítica..." | Segurança | Fluxo em diagrama |
| 08:15–09:00 | Métricas | Mostrar impacto | "O sistema estima..." | Pensamento crítico | Números em slide |

---

## 5. Respostas Objetivas às Perguntas Obrigatórias

### 1. Qual LLM você escolheu e por quê?

"Escolhi o GPT-4o da OpenAI. É o modelo mais capaz disponível, com excelente compreensão de contexto jurídico, suporte nativo ao português brasileiro, e capacidade de gerar JSON estruturado consistentemente. Além disso, oferece embeddings de alta qualidade através do modelo text-embedding-3-small. A temperatura foi configurada em 0.3 para reduzir criatividade e aumentar consistência. O modelo responde em 2-5 segundos típicamente, o que é aceitável para um MVP."

**Tempo**: ~45 segundos

---

### 2. Como sua solução utiliza Engenharia de Prompts?

"A engenharia de prompts é crítica nesta solução. Cada prompt define um contrato de comportamento com o modelo. Por exemplo, o prompt de extração especifica exatamente o formato JSON esperado, as regras para identificar partes e datas, e a instrução 'Nunca invente informações'. O prompt do sistema define o papel do assistente, as regras de rastreabilidade, e a instrução de sempre citar fontes. Cada palavra importa. Se eu remover a regra 'Nunca invente', o modelo pode começar a alucinar. A engenharia de prompts reduz alucinações e aumenta a previsibilidade das respostas."

**Tempo**: ~50 segundos

---

### 3. Como o agente decide quais ações executar?

"Tecnicamente, este sistema não implementa um agente autônomo com tool calling. Implementa um fluxo orquestrado determinístico. O Agent Router classifica a intenção do usuário usando palavras-chave — se a pergunta contém 'resumo', executa a ferramenta de resumo; se contém 'risco', executa a análise de riscos. O backend escolhe o prompt apropriado, recupera os documentos necessários, chama o modelo, valida a saída, e devolve o resultado.

Isso é diferente de um agente com function calling, onde o modelo decide autonomamente quais ferramentas usar. Neste MVP, a decisão é determinística. Mas a arquitetura permite evoluir para um agente com function calling, onde o modelo GPT-4 teria acesso às ferramentas e decidiria autonomamente qual usar."

**Tempo**: ~60 segundos

---

### 4. Como você estruturaria uma solução utilizando RAG para documentos jurídicos?

"RAG é fundamental para documentos jurídicos. Primeiro, extrair o texto do PDF e dividir em chunks com sobreposição — isso garante que informações que atravessam limites de chunks não sejam perdidas. Segundo, gerar embeddings para cada chunk usando um modelo de embeddings de alta qualidade. Terceiro, armazenar os chunks e embeddings em um banco vetorial — SQLite para MVP, pgvector ou Qdrant para produção.

Quando uma pergunta chega, gerar embedding da pergunta, recuperar os chunks mais similares, e enviar o contexto ao modelo. O modelo gera a resposta baseada apenas nesse contexto.

Para documentos jurídicos especificamente, eu adicionaria: filtros por cliente para segregação de dados, reranking para melhorar precisão, busca híbrida combinando semântica com palavras-chave, e validação de confiança para bloquear respostas sem evidência suficiente."

**Tempo**: ~60 segundos

---

### 5. Como evita alucinações da IA?

"Implemento três camadas de proteção. Primeira, engenharia de prompts rigorosa — o prompt diz explicitamente 'Nunca invente informações' e 'Se não encontrar, diga que não encontrou'. Segunda, recuperação de contexto — o modelo recebe apenas os trechos relevantes do documento, reduzindo o espaço para invenção. Terceira, validação determinística — após a resposta, o sistema calcula um score de confiança baseado em: quantidade de chunks recuperados, similaridade média, quantidade de citações, consistência entre resposta e contexto, e qualidade do contexto.

Se o score cair abaixo de 60 pontos, a resposta é bloqueada. O usuário recebe a mensagem: 'Não encontrei evidências suficientes nos documentos selecionados para responder com segurança.'

Importante: nenhuma solução baseada em LLM elimina totalmente as alucinações. O objetivo é reduzir o espaço para invenção e manter o profissional jurídico responsável pela validação final."

**Tempo**: ~70 segundos

---

### 6. Como monitora falhas e erros da solução?

"O sistema implementa logging estruturado em JSON. Cada operação crítica — upload, extração, chat, análise — é registrada com timestamp, tipo de evento, duração, e resultado. Se um erro ocorre, é registrado com stack trace.

Atualmente, os logs são salvos em arquivo. Para produção, eu integraria Sentry para rastreamento de exceções, OpenTelemetry para rastreamento distribuído, Prometheus para métricas, e Grafana para visualização.

Além disso, o sistema persiste o status de cada análise — GERADA, PENDENTE_REVISÃO, APROVADA, REJEITADA. Isso permite rastrear o fluxo completo de uma análise. E há um endpoint de health check que verifica se o backend está respondendo."

**Tempo**: ~55 segundos

---

### 7. Se essa solução fosse utilizada por um escritório de advocacia, quais cuidados adicionais seriam necessários em relação à segurança, confiabilidade e privacidade?

"Muitos cuidados. Primeiro, LGPD compliance — política de retenção de dados, direito ao esquecimento, consentimento explícito. Segundo, criptografia — em repouso (dados no banco) e em trânsito (HTTPS obrigatório). Terceiro, segregação de dados — cada cliente em um espaço isolado, garantindo que um cliente nunca veja documentos de outro.

Quarto, autenticação robusta — MFA (autenticação de dois fatores), não apenas JWT. Quinto, auditoria detalhada — quem acessou qual documento, quando, e o quê fez. Sexto, validação de arquivos — antivírus, detecção de malware, limite de tamanho.

Sétimo, contrato com OpenAI — garantias sobre uso de dados, residência de dados, conformidade com LGPD. Oitavo, revisão jurídica — validação com especialistas em direito digital e LGPD.

Nono, backup e recuperação de desastre — garantir que dados não sejam perdidos. Décimo, prevenção de prompt injection — validar entrada do usuário para evitar que alguém injete instruções maliciosas no prompt.

Este MVP implementa autenticação JWT, RBAC, ownership enforcement, e logging. Mas uma implantação real exigiria todos esses controles adicionais."

**Tempo**: ~90 segundos

---

## 6. Perguntas Técnicas que Podem Ser Feitas Depois

1. **Por que escolher GPT-4o em vez de GPT-4-turbo ou Claude?**
   - Resposta: GPT-4o oferece melhor relação custo-benefício, suporte nativo ao português, e capacidade de gerar JSON estruturado. Claude seria uma alternativa válida, mas teria custo maior.

2. **Como você calibraria o threshold de confiança (60 pontos)?**
   - Resposta: Com dados reais de usuários. Começaria com 60 e ajustaria baseado em feedback — se muitas respostas bloqueadas são na verdade corretas, abaixaria o threshold; se muitas respostas permitidas têm erros, aumentaria.

3. **Por que usar SQLite em vez de PostgreSQL desde o início?**
   - Resposta: SQLite é adequado para MVP — sem dependências externas, fácil de configurar. PostgreSQL seria necessário para produção com múltiplos usuários simultâneos.

4. **Como você escalaria a solução para processar 1000 contratos por dia?**
   - Resposta: Implementaria fila de processamento (Celery/RabbitMQ), cache de embeddings, pgvector para busca vetorial otimizada, e load balancing no backend.

5. **Como você detectaria se o modelo está alucinando?**
   - Resposta: Através do score de confiança. Se a resposta tem baixa similaridade com os chunks recuperados, é provável que esteja alucinando. Além disso, testes com dados conhecidos.

6. **Por que usar text-embedding-3-small em vez de text-embedding-3-large?**
   - Resposta: Small é suficiente para documentos jurídicos, tem custo menor, e é mais rápido. Large seria necessário apenas se a precisão fosse crítica.

7. **Como você trataria documentos muito longos (>100 páginas)?**
   - Resposta: O chunking com sobreposição já lida bem. Mas para documentos muito longos, eu implementaria sumarização prévia ou filtragem por seção.

8. **Como você integraria com sistemas jurídicos existentes (ex: Salesforce, SAP)?**
   - Resposta: Através de APIs REST. O backend expõe endpoints que podem ser consumidos por qualquer sistema. Ou usar webhooks para notificar sistemas externos quando uma análise é concluída.

9. **Como você mediria o impacto real da solução?**
   - Resposta: Através de métricas: tempo médio de análise antes e depois, precisão da recuperação, taxa de respostas aceitas pelo usuário, quantidade de revisões necessárias, custo por documento, latência, taxa de erros, satisfação do usuário.

10. **Como você trataria conflitos de interesse (ex: um advogado vendo documentos de um cliente concorrente)?**
    - Resposta: Através de segregação de dados rigorosa e auditoria. Cada cliente teria um espaço isolado. Qualquer acesso cruzado seria registrado e auditado.

11. **Como você garantiria que o modelo não vaza informações confidenciais?**
    - Resposta: Não enviando dados confidenciais para a API da OpenAI. Ao invés disso, usar um modelo local (ex: Llama) ou garantir contrato com OpenAI sobre retenção de dados.

12. **Como você trataria PDFs com imagens ou tabelas complexas?**
    - Resposta: Atualmente, o sistema não tem OCR. Para produção, integraria Tesseract ou AWS Textract para extrair texto de imagens.

13. **Como você validaria que a extração de informações está correta?**
    - Resposta: Através de testes com contratos conhecidos, validação humana, e métricas de precisão. Além disso, o score de confiança ajuda a identificar extrações questionáveis.

14. **Como você trataria múltiplas versões do mesmo contrato?**
    - Resposta: O sistema já suporta versionamento estrutural. Cada versão é um documento separado. A comparação permite identificar mudanças entre versões.

15. **Como você implementaria aprovação em múltiplos níveis (ex: junior, senior, partner)?**
    - Resposta: Estendendo o modelo AnalysisReview com um campo de nível de aprovação. Cada nível teria permissões diferentes.

16. **Como você trataria análises que levam muito tempo (>30 segundos)?**
    - Resposta: Implementando processamento assíncrono com notificações. O usuário não fica esperando — recebe uma notificação quando a análise está pronta.

17. **Como você mediria a qualidade das respostas do modelo?**
    - Resposta: Através de testes com dados conhecidos, feedback dos usuários, e comparação com análises manuais de especialistas.

18. **Como você trataria atualizações do modelo GPT-4?**
    - Resposta: A arquitetura permite trocar o modelo facilmente. Testaria a nova versão em paralelo antes de fazer rollout.

19. **Como você implementaria um sistema de feedback para melhorar o modelo?**
    - Resposta: Capturando feedback dos usuários (aprovação/rejeição), armazenando em um banco de dados, e usando para fine-tuning ou retraining.

20. **Como você garantiria conformidade com LGPD em relação a direito ao esquecimento?**
    - Resposta: Implementando um endpoint de deleção que remove todos os dados de um usuário — documentos, chunks, embeddings, análises, reviews. Tudo seria deletado de forma segura.

---

## 7. Roteiro Corrido para Teleprompter

[Abertura]

Olá, meu nome é Leonardo Fragoso. Neste vídeo vou apresentar o Legal AI Copilot, uma solução que desenvolvi para automatizar a análise de documentos jurídicos utilizando Inteligência Artificial generativa, recuperação semântica e prompts estruturados.

O projeto nasceu de um problema real: advogados e equipes jurídicas gastam horas lendo contratos extensos, extraindo informações-chave, identificando riscos e comparando cláusulas. Este trabalho é repetitivo, propenso a erros e consome tempo que poderia ser dedicado à análise estratégica.

Nesta demonstração, vou mostrar como a solução transforma um contrato em informações estruturadas, rastreáveis e revisáveis, mantendo sempre o profissional jurídico no controle da decisão final.

[Pausa]

O desafio é transformar documentos jurídicos extensos em informações estruturadas sem perder a rastreabilidade. A solução combina três pilares:

Primeiro, Recuperação Semântica: quando um usuário faz uma pergunta, o sistema não processa o documento inteiro. Ele recupera apenas os trechos mais relevantes usando embeddings e similaridade de cosseno.

Segundo, IA Generativa Estruturada: o modelo GPT-4 recebe o contexto recuperado e gera respostas em formato estruturado — JSON com partes, datas, valores e cláusulas.

Terceiro, Guardrails e Revisão Humana: a resposta é validada contra as fontes. Se não houver evidência suficiente, o sistema bloqueia a resposta. Todas as análises são persistidas e podem ser aprovadas ou rejeitadas por um profissional jurídico.

A stack é Python com FastAPI no backend, React no frontend, SQLite para persistência, e OpenAI para o modelo de linguagem.

[Pausa]

A arquitetura segue um padrão clássico com camadas bem definidas. No frontend, temos uma interface React que permite fazer login, enviar documentos e interagir com o sistema.

No backend, a API FastAPI orquestra todo o fluxo. Quando um contrato é enviado, o sistema extrai o texto, divide em chunks com sobreposição, e gera embeddings — representações vetoriais que capturam o significado semântico.

Esses embeddings são armazenados no SQLite junto com os chunks. Quando uma pergunta chega, o sistema recupera os chunks mais similares usando cálculo de similaridade de cosseno.

O contexto recuperado é enviado ao modelo GPT-4 junto com um prompt estruturado. O modelo gera a resposta, que passa por validação de confiança antes de ser retornada.

Todas as análises são persistidas com histórico completo, permitindo revisão humana e rastreabilidade.

[Trocar para a aplicação]

Vou começar fazendo login na plataforma com as credenciais de demonstração. Após autenticação, o advogado acessa o dashboard onde pode ver todos os seus documentos e iniciar análises. A autenticação é baseada em JWT com tokens que expiram em 30 minutos, e o sistema implementa controle de acesso por papéis.

[Pausa]

Vou fazer upload de um contrato de prestação de serviços. O sistema extrai o texto automaticamente, divide em chunks inteligentes com sobreposição, e gera embeddings para cada chunk. Tudo isso acontece de forma assíncrona, então o usuário não fica esperando.

[Pausa]

Quando envio a pergunta, o sistema gera um embedding da pergunta, compara com todos os chunks usando similaridade de cosseno, recupera os trechos mais relevantes, e envia ao modelo GPT-4 junto com um prompt estruturado.

O modelo gera a resposta, que passa por validação. O sistema verifica se existem chunks recuperados, se a resposta cita as fontes, se o score de similaridade é adequado, e se a confiança é suficiente.

A resposta é retornada com um score de confiança — neste caso, 85 pontos, o que significa alta sustentação documental. As citações mostram exatamente de qual trecho do documento a resposta foi extraída. Isso é crucial em contexto jurídico.

[Pausa]

A análise de riscos identifica cláusulas problemáticas usando um mecanismo determinístico baseado em palavras-chave. Neste contrato, o sistema identificou cinco riscos: multa ilimitada (crítico), falta de cláusula de confidencialidade (médio), falta de conformidade LGPD (alto), renovação automática (médio), e pagamento indefinido (alto).

Cada risco vem com uma recomendação de ação. Este mecanismo é determinístico — não depende de LLM — então é rápido e previsível. Mas é importante notar que é uma primeira camada de análise. O profissional jurídico sempre revisa e valida os riscos identificados.

[Pausa]

A extração estruturada transforma o texto livre do contrato em dados estruturados — JSON com campos bem definidos. O sistema identifica partes (quem contrata quem), datas (início, término, renovação), valores (salários, custos, multas), e cláusulas principais.

Isso permite que o profissional jurídico veja rapidamente os termos-chave sem precisar ler o contrato inteiro. E porque os dados são estruturados, podem ser exportados ou integrados com outros sistemas.

[Pausa]

Quando um profissional jurídico precisa comparar duas versões de um contrato, o sistema automatiza essa tarefa. Ele identifica as similaridades, as diferenças e gera um resumo executivo. Isso economiza tempo significativo em negociações.

[Pausa]

Vou mostrar como a engenharia de prompts funciona. [Mostrar o prompt no código]

O prompt tem várias seções: Definição de Papel, Regras Importantes, e Formato de Resposta. Engenharia de prompts não é apenas escrever uma pergunta — é criar um contrato de comportamento com o modelo.

Além do prompt, o sistema implementa guardrails — validações determinísticas que bloqueiam respostas sem evidência suficiente.

O score de confiança é calculado assim: Fontes (até 30 pontos), Similaridade (até 30 pontos), Citações (até 20 pontos), Consistência (até 10 pontos), e Qualidade (até 10 pontos).

Se o score cair abaixo de 60 pontos, a resposta é bloqueada. Melhor dizer 'não sei' do que inventar uma resposta que pode ter consequências legais.

[Pausa]

RAG — Retrieval-Augmented Generation — é o coração desta solução. Quando um contrato é enviado, o sistema extrai o texto, divide em chunks de 1000 caracteres com 20% de sobreposição, e gera embeddings usando o modelo text-embedding-3-small da OpenAI.

Cada chunk vira um vetor de 1536 dimensões que captura seu significado semântico. Quando uma pergunta chega, o sistema gera embedding da pergunta, calcula similaridade de cosseno com todos os embeddings dos chunks, recupera os top-5 chunks mais similares, e envia o contexto ao modelo GPT-4.

Por que isso funciona? Porque o embedding captura significado semântico. Uma pergunta como 'Qual é o custo?' será similar a um chunk que diz 'O valor total é R$ 50.000'. Não é busca por palavras-chave — é busca por significado.

Neste MVP, usamos SQLite com cálculo de similaridade em memória. Para produção, eu implementaria pgvector, Qdrant, busca híbrida, e reranking. Isso aumentaria a precisão e a escalabilidade.

[Pausa]

Uma característica crítica desta solução é a revisão humana obrigatória. Nenhuma análise gerada pela IA é considerada final sem aprovação de um profissional jurídico.

Todas as análises são persistidas em um banco de dados com histórico completo. Um advogado pode aprovar, rejeitar, ou solicitar mudanças. Cada decisão é registrada com timestamp, nome do revisor e comentário. Isso cria uma trilha de auditoria completa.

Em termos de segurança: autenticação JWT, RBAC, ownership enforcement, sem dados sensíveis em logs, senhas com hash Argon2.

Para uma implantação real em um escritório de advocacia, eu adicionaria: LGPD compliance, criptografia em repouso, criptografia em trânsito, segregação de dados por cliente, auditoria detalhada, validação de arquivos, contrato com OpenAI, e revisão jurídica.

[Pausa]

O sistema estima o tempo economizado em cada análise. Para um resumo, o tempo manual estimado é 30 minutos. Com a automação, 2-3 segundos. Para uma extração, 45 minutos manualmente, 3-5 segundos com automação. Para uma comparação, 90 minutos manualmente, 5-10 segundos com automação.

Isso não significa que o profissional economiza 30 minutos por resumo — ele ainda precisa revisar e validar. Mas a automação reduz o trabalho repetitivo, permitindo que ele dedique tempo à análise estratégica.

Este é um MVP — uma prova de conceito. Algumas funcionalidades ainda podem evoluir. Mas a arquitetura foi projetada para evoluir. Cada componente é modular e pode ser substituído ou melhorado sem afetar o resto do sistema.

Com este projeto, procurei demonstrar não apenas uma integração com um modelo de linguagem, mas a construção de um fluxo completo — desde o processamento dos documentos até a entrega de uma resposta contextualizada, rastreável e revisável.

A solução ainda pode evoluir em observabilidade, segurança e avaliação contínua. Mas o MVP valida a arquitetura e mostra como a IA pode reduzir atividades repetitivas sem retirar do profissional jurídico a responsabilidade pela decisão final.

Obrigado.

---

## 8. Versão Resumida de Emergência (5 minutos)

[Se o vídeo estiver ultrapassando o limite, usar esta versão]

Olá, meu nome é Leonardo Fragoso. Desenvolvi o Legal AI Copilot, uma solução que automatiza a análise de documentos jurídicos usando IA generativa e recuperação semântica.

O problema: advogados gastam horas lendo contratos, extraindo informações e identificando riscos. A solução: um sistema que transforma contratos em informações estruturadas, rastreáveis e revisáveis.

[Trocar para a aplicação]

Vou fazer login e fazer upload de um contrato. O sistema extrai o texto, divide em chunks, gera embeddings, e armazena no banco de dados.

[Mostrar upload]

Agora vou fazer uma pergunta ao sistema. Quando envio a pergunta, o sistema recupera os trechos mais relevantes usando busca semântica, envia ao modelo GPT-4 junto com um prompt estruturado, e retorna uma resposta com score de confiança e citações.

[Mostrar resposta]

A análise de riscos identifica cláusulas problemáticas. Neste contrato, encontrou multa ilimitada, falta de cláusula de confidencialidade, e falta de conformidade LGPD.

[Mostrar análise de riscos]

A extração estruturada transforma o texto em JSON com partes, datas, valores e cláusulas.

[Mostrar extração]

A engenharia de prompts é crítica. O prompt define um contrato de comportamento com o modelo — especifica o formato, as regras, e a instrução de nunca inventar informações.

RAG — Retrieval-Augmented Generation — é o coração da solução. O sistema gera embeddings dos chunks, recupera os mais similares, e envia o contexto ao modelo. Isso reduz alucinações porque o modelo só pode responder baseado no contexto recuperado.

O score de confiança é calculado baseado em: quantidade de chunks recuperados, similaridade média, quantidade de citações, consistência, e qualidade do contexto. Se o score cair abaixo de 60 pontos, a resposta é bloqueada.

[Mostrar revisão]

Todas as análises passam por revisão humana obrigatória. Um advogado pode aprovar, rejeitar, ou solicitar mudanças. Cada decisão é registrada com timestamp e comentário.

Em termos de segurança: autenticação JWT, RBAC, ownership enforcement, e logging estruturado. Para produção, adicionaria LGPD compliance, criptografia, segregação de dados por cliente, e auditoria detalhada.

O sistema estima o tempo economizado: 30 minutos para um resumo manual, 2-3 segundos com automação. 45 minutos para extração manual, 3-5 segundos com automação.

Este é um MVP que valida a arquitetura. Mostra como a IA pode reduzir atividades repetitivas sem retirar do profissional jurídico a responsabilidade pela decisão final.

Obrigado.

---

## 9. Evidências Técnicas Encontradas no Repositório

| Afirmação | Arquivo | Evidência |
|-----------|---------|-----------|
| A aplicação gera embeddings | `backend/app/embedding_service.py` | Classe `EmbeddingService` com método `generate_embedding()` usando OpenAI |
| O sistema utiliza SQLite | `backend/app/database.py` | Configuração de banco de dados SQLite |
| Existe busca semântica | `backend/app/legal_agent.py:86-89` | Função `_cosine_similarity()` para cálculo de similaridade |
| Implementa autenticação JWT | `backend/app/auth.py` | Funções `create_access_token()` e `verify_token()` |
| Implementa RBAC | `backend/app/models.py` | Enum `UserRole` com ADMIN, LAWYER, ASSISTANT, CLIENT, VIEWER |
| Chunking com sobreposição | `backend/app/chunker.py` | Classe `Chunker` com parâmetros `chunk_size=1000, overlap=200` |
| Análise de riscos heurística | `backend/app/risk_analysis.py:1-110` | Classe `HeuristicAnalyzer` com palavras-chave para detecção de riscos |
| Guardrails e validação | `backend/app/ai_validator.py` | Classe `AIValidator` com cálculo de score de confiança |
| Revisão humana | `backend/app/models.py` | Modelos `AnalysisRecord` e `AnalysisReview` |
| Automação pós-upload | `backend/app/automation_service.py` | Função `run_post_upload_automation()` |
| Webhook para n8n | `backend/app/webhook_service.py` | Classe `WebhookService` com envio de eventos |
| Testes automatizados | `backend/tests/test_demo_smoke.py` | 166 testes passando |
| Extração de PDF | `backend/app/pdf_extractor.py` | Classe `PDFExtractor` usando PyPDF |
| Modelo GPT-4o | `backend/app/legal_agent.py:116-120` | `ChatOpenAI(model="gpt-4o", temperature=0.3)` |
| Prompt estruturado | `backend/app/legal_agent.py:153-184` | Prompt de extração com JSON estruturado |
| Frontend React | `frontend/src/` | Aplicação React com TypeScript |
| Migrations Alembic | `backend/alembic/versions/` | Múltiplas migrações para criar tabelas |

---

## 10. Pontos que NÃO Devem Ser Afirmados

| Não Afirmar | Forma Correta |
|-------------|---------------|
| "A solução elimina alucinações." | "A solução utiliza mecanismos para reduzir alucinações e mantém revisão humana." |
| "O sistema já está pronto para grandes escritórios." | "O MVP valida a arquitetura, mas uma implantação real exigiria controles adicionais." |
| "A análise de riscos usa LLM." | "A análise de riscos é determinística, baseada em palavras-chave." |
| "Existe um banco vetorial dedicado." | "Usamos SQLite com cálculo de similaridade em memória. Para produção, seria pgvector ou Qdrant." |
| "O sistema processa OCR." | "O sistema não tem OCR — apenas extração de texto de PDFs digitalizados." |
| "Implementamos refresh token auto-refresh." | "Frontend redireciona para login em 401. Não há silent refresh." |
| "Temos testes frontend automatizados." | "Frontend validado via build TypeScript. Sem testes automatizados." |
| "Métricas são calibradas com dados reais." | "Métricas são estimativas do MVP, não calibradas com dados reais." |
| "Versioning com regeneração automática." | "Versioning estrutural apenas. Sem regeneração automática." |
| "A solução substitui advogados." | "A solução apoia o profissional jurídico, não o substitui." |

---

## 11. Riscos Antes da Gravação

### Riscos Identificados

1. **OPENAI_API_KEY não configurada**
   - **Impacto**: Chat, resumo, extração e comparação não funcionam
   - **Mitigation**: Verificar `.env` antes de gravar. Sistema funciona em modo heurístico (análise de riscos).
   - **Plano B**: Mostrar análise de riscos (determinística) e explicar que as outras funcionalidades usam o mesmo pipeline

2. **Banco de dados corrompido**
   - **Impacto**: Aplicação não inicia
   - **Mitigation**: Deletar `legal_ai.db` e recriar com `alembic upgrade head && python -m app.seed`
   - **Tempo**: ~30 segundos

3. **Porta 8000 ou 5173 já em uso**
   - **Impacto**: Backend ou frontend não inicia
   - **Mitigation**: Verificar processos em execução, matar se necessário
   - **Comando**: `lsof -i :8000` e `lsof -i :5173`

4. **Latência alta na primeira chamada ao OpenAI**
   - **Impacto**: Vídeo parece travado
   - **Mitigation**: Fazer uma chamada de aquecimento antes de gravar
   - **Fala**: "A primeira chamada ao modelo pode levar alguns segundos enquanto a conexão é estabelecida."

5. **Arquivo de contrato não encontrado**
   - **Impacto**: Upload falha
   - **Mitigation**: Verificar se `Contrato_Prestacao_Servicos_Teste.pdf` existe no diretório raiz
   - **Plano B**: Usar `contrato.pdf` ou criar um arquivo de teste

6. **Erro de permissão no banco de dados**
   - **Impacto**: Não consegue escrever no banco
   - **Mitigation**: Verificar permissões do arquivo `legal_ai.db`
   - **Comando**: `chmod 644 legal_ai.db`

### Checklist de Validação Pré-Gravação

- [ ] OPENAI_API_KEY configurada e testada
- [ ] Backend iniciado e respondendo
- [ ] Frontend iniciado e acessível
- [ ] Banco de dados inicializado
- [ ] Usuários demo criados
- [ ] Arquivo de contrato disponível
- [ ] Testes passando: `pytest tests/test_demo_smoke.py -v`
- [ ] Nenhuma porta em conflito
- [ ] Credenciais demo memorizadas
- [ ] Planos alternativos revisados

---

## 12. Resumo de Funcionalidades Confirmadas

### Implementadas e Funcionais
✅ Autenticação JWT com RBAC  
✅ Upload de PDF com extração de texto  
✅ Chunking com sobreposição  
✅ Geração de embeddings (OpenAI)  
✅ Busca semântica com similaridade de cosseno  
✅ Chat com RAG  
✅ Resumo de documentos  
✅ Extração estruturada (JSON)  
✅ Comparação de contratos  
✅ Análise de riscos (heurística)  
✅ Guardrails e validação de confiança  
✅ Revisão humana com state machine  
✅ Métricas de impacto  
✅ Automação pós-upload  
✅ Webhooks para n8n  
✅ Logging estruturado  
✅ 166 testes automatizados

### Limitações Conhecidas
❌ Sem OCR (apenas PDFs digitalizados)  
❌ Análise de riscos é determinística (não usa LLM)  
❌ Sem refresh token auto-refresh  
❌ Sem testes frontend automatizados  
❌ SQLite (não escalável para produção)  
❌ Sem integração com sistemas jurídicos externos  
❌ Métricas são estimativas, não calibradas  
❌ Versioning estrutural apenas (sem regeneração automática)

---

## 13. Tempo Estimado do Roteiro

- **Roteiro principal**: 7-9 minutos (alvo: 8 minutos)
- **Versão resumida**: 5 minutos
- **Abertura**: 45 segundos
- **Demonstração funcional**: 3 minutos 15 segundos
- **Explicações técnicas**: 3 minutos

---

## 14. Conclusão

Este roteiro foi elaborado com base em uma auditoria completa do repositório Legal AI Copilot. Todas as funcionalidades mencionadas foram verificadas no código. Nenhuma funcionalidade foi inventada.

O vídeo deve demonstrar:
1. **Visão de produto**: Entender o problema e a solução
2. **Domínio técnico**: Explicar arquitetura, RAG, embeddings, prompts
3. **Implementação prática**: Mostrar a aplicação funcionando
4. **Responsabilidade jurídica**: Enfatizar revisão humana, guardrails, segurança
5. **Honestidade**: Reconhecer limitações e propor evoluções

Leonardo está pronto para gravar.
