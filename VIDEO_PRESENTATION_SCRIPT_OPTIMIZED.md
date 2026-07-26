# Roteiro Otimizado para Vídeo — Legal AI Copilot

**Versão**: Otimizada para 7-9 minutos  
**Duração Alvo**: 8 minutos (1280 palavras)  
**Abordagem**: Demonstração prática + explicações breves

---

## Abertura (00:00–00:30) — 60 palavras

"Olá, meu nome é Leonardo Fragoso. Desenvolvi o Legal AI Copilot, uma solução que automatiza a análise de documentos jurídicos usando IA generativa e recuperação semântica. O projeto resolve um problema real: advogados gastam horas lendo contratos, extraindo informações e identificando riscos. Nesta demonstração, vou mostrar como o sistema transforma um contrato em informações estruturadas, rastreáveis e revisáveis."

---

## Problema e Solução (00:30–01:15) — 90 palavras

"A solução combina três pilares. Primeiro, recuperação semântica: o sistema recupera apenas os trechos relevantes do documento usando embeddings. Segundo, IA generativa estruturada: o modelo GPT-4 gera respostas em JSON com partes, datas, valores e cláusulas. Terceiro, guardrails: a resposta é validada contra as fontes. Se não houver evidência suficiente, o sistema bloqueia a resposta. Todas as análises são persistidas e podem ser aprovadas ou rejeitadas por um profissional jurídico."

---

## Demonstração: Login (01:15–01:45) — 60 palavras

[AÇÃO: Abrir frontend, fazer login]

"Vou fazer login na plataforma. O sistema usa autenticação JWT com tokens que expiram em 30 minutos. Após autenticação, o advogado acessa o dashboard onde pode ver seus documentos e iniciar análises. O sistema implementa controle de acesso por papéis — advogados, assistentes, administradores e visualizadores têm permissões diferentes."

---

## Demonstração: Upload (01:45–02:30) — 90 palavras

[AÇÃO: Upload de PDF, aguardar processamento]

"Vou fazer upload de um contrato. O sistema extrai o texto automaticamente, divide em chunks de tamanho inteligente, e gera embeddings — representações vetoriais que capturam o significado semântico. Esses embeddings são armazenados no banco junto com os chunks. Tudo isso acontece de forma assíncrona, então o usuário não fica esperando. Após o processamento, o documento está pronto para análise."

---

## Demonstração: Chat com RAG (02:30–04:00) — 180 palavras

[AÇÃO: Abrir chat, fazer pergunta, mostrar resposta]

"Agora vou fazer uma pergunta ao sistema: 'Qual é o valor total do contrato?' Quando envio a pergunta, o sistema gera um embedding da pergunta, compara com todos os chunks usando similaridade de cosseno, recupera os trechos mais relevantes, e envia ao modelo GPT-4 junto com um prompt estruturado.

O modelo gera a resposta, que passa por validação. O sistema verifica se existem chunks recuperados, se a resposta cita as fontes, se o score de similaridade é adequado, e se a confiança é suficiente.

A resposta é retornada com um score de confiança — neste caso, 85 pontos, o que significa alta sustentação documental. As citações mostram exatamente de qual trecho do documento a resposta foi extraída. Isso é crucial em contexto jurídico — o profissional pode verificar a fonte imediatamente.

Se a pergunta não tiver resposta no documento, o sistema bloqueia a resposta e diz 'Não encontrei evidências suficientes'. Isso reduz alucinações porque o modelo só pode responder baseado no contexto recuperado."

---

## Demonstração: Análise de Riscos (04:00–04:45) — 90 palavras

[AÇÃO: Executar análise de riscos, mostrar resultados]

"A análise de riscos identifica cláusulas problemáticas usando um mecanismo determinístico baseado em palavras-chave. Neste contrato, o sistema identificou cinco riscos: multa ilimitada (crítico), falta de cláusula de confidencialidade (médio), falta de conformidade LGPD (alto), renovação automática (médio), e pagamento indefinido (alto).

Cada risco vem com uma recomendação de ação. Este mecanismo é determinístico — não depende de LLM — então é rápido e previsível. Mas é importante notar que é uma primeira camada de análise. O profissional jurídico sempre revisa e valida os riscos identificados."

---

## Demonstração: Extração e Comparação (04:45–05:45) — 120 palavras

[AÇÃO: Mostrar extração estruturada, depois comparação]

"A extração estruturada transforma o texto livre em dados estruturados — JSON com campos bem definidos. O sistema identifica partes, datas, valores e cláusulas principais. Isso permite que o profissional veja rapidamente os termos-chave sem precisar ler o contrato inteiro.

Quando um profissional precisa comparar duas versões de um contrato, o sistema automatiza essa tarefa. Ele identifica as similaridades, as diferenças e gera um resumo executivo. Isso economiza tempo significativo em negociações onde múltiplas versões são trocadas.

Todas essas análises são persistidas em um banco de dados com histórico completo, permitindo revisão humana e rastreabilidade."

---

## Engenharia de Prompts e Guardrails (05:45–06:45) — 120 palavras

[AÇÃO: Mostrar prompt no código ou slide]

"A engenharia de prompts é crítica nesta solução. O prompt define um contrato de comportamento com o modelo. Ele diz: 'Responda baseado apenas nas informações fornecidas. Se a informação não estiver disponível, diga que não encontrou.' Cada palavra importa.

O sistema implementa guardrails — validações determinísticas que bloqueiam respostas sem evidência suficiente. O score de confiança é calculado baseado em cinco componentes: quantidade de chunks recuperados, similaridade média, quantidade de citações, consistência entre resposta e contexto, e qualidade do contexto.

Se o score cair abaixo de 60 pontos, a resposta é bloqueada. Melhor dizer 'não sei' do que inventar uma resposta que pode ter consequências legais."

---

## Revisão Humana e Resultados (06:45–07:45) — 120 palavras

[AÇÃO: Mostrar página de revisões, demonstrar aprovação]

"Uma característica crítica desta solução é a revisão humana obrigatória. Nenhuma análise gerada pela IA é considerada final sem aprovação de um profissional jurídico.

Todas as análises são persistidas em um banco de dados com histórico completo. Um advogado pode aprovar, rejeitar, ou solicitar mudanças. Cada decisão é registrada com timestamp, nome do revisor e comentário. Isso cria uma trilha de auditoria completa.

O sistema estima o tempo economizado em cada análise. Para um resumo, o tempo manual estimado é 30 minutos. Com a automação, 2-3 segundos. Para uma extração, 45 minutos manualmente, 3-5 segundos com automação.

Este é um MVP que valida a arquitetura. Mostra como a IA pode reduzir atividades repetitivas sem retirar do profissional jurídico a responsabilidade pela decisão final."

---

## Fechamento (07:45–08:00) — 40 palavras

"A solução ainda pode evoluir em observabilidade, segurança e avaliação contínua. Mas o MVP valida a arquitetura e demonstra o potencial de IA para transformar a prática jurídica. Obrigado."

---

## Resumo de Duração

```
Abertura: 60 palavras = 30 segundos
Problema: 90 palavras = 45 segundos
Login: 60 palavras = 30 segundos
Upload: 90 palavras = 45 segundos
Chat RAG: 180 palavras = 90 segundos
Análise Riscos: 90 palavras = 45 segundos
Extração/Comparação: 120 palavras = 60 segundos
Prompts/Guardrails: 120 palavras = 60 segundos
Revisão/Resultados: 120 palavras = 60 segundos
Fechamento: 40 palavras = 20 segundos

TOTAL: 970 palavras ≈ 8 minutos (a 120 WPM)
```

---

## Sequência Exata de Cliques

### 1. Login
1. Abrir `http://localhost:5173`
2. Clicar em "Entrar"
3. Email: `lawyer@demo.com`
4. Senha: `demo123456`
5. Clicar em "Entrar"
6. Aguardar carregamento do dashboard

### 2. Upload
1. Clicar em "Novo Documento" ou "Upload"
2. Selecionar `Contrato_Prestacao_Servicos_Teste.pdf`
3. Título: "Contrato de Prestação de Serviços"
4. Clicar em "Enviar"
5. Aguardar status mudar para "Processado" (2-3 segundos)

### 3. Chat
1. Clicar no documento
2. Clicar em "Chat"
3. Digitar: "Qual é o valor total do contrato?"
4. Clicar em "Enviar"
5. Aguardar resposta (3-5 segundos)
6. Mostrar score de confiança e citações

### 4. Análise de Riscos
1. Clicar em "Análise de Riscos"
2. Clicar em "Analisar"
3. Aguardar resultado (1-2 segundos)
4. Mostrar lista de riscos

### 5. Extração
1. Clicar em "Extração"
2. Clicar em "Extrair"
3. Aguardar resultado (3-5 segundos)
4. Mostrar JSON estruturado

### 6. Comparação
1. Clicar em "Comparação"
2. Selecionar segundo contrato
3. Clicar em "Comparar"
4. Mostrar diferenças

### 7. Revisão
1. Clicar em "Revisões"
2. Selecionar uma análise
3. Clicar em "Aprovar"
4. Mostrar histórico de revisão

---

## Planos Alternativos

### Se OpenAI API falhar
- Demonstrar análise de riscos (determinística, sem LLM)
- Fala: "A análise de riscos funciona independentemente da API de IA generativa"

### Se upload falhar
- Usar documento pré-carregado
- Fala: "Aqui temos um contrato que foi processado anteriormente"

### Se chat não responder
- Mostrar resultado pré-gravado
- Fala: "Vou mostrar um resultado típico do sistema"

### Se frontend não carregar
- Usar API via Swagger
- Fala: "Vou demonstrar a funcionalidade através da API REST"

---

## Perguntas Obrigatórias Respondidas no Vídeo

| Pergunta | Momento | Resposta Breve |
|----------|---------|---|
| Qual LLM? | Chat RAG | GPT-4o, temperatura 0.3 |
| Engenharia de Prompts? | Seção 8 | Prompt estruturado com regras de rastreabilidade |
| Como o agente decide? | Chat RAG | Recupera chunks, envia ao modelo com contexto |
| Como estruturar RAG jurídico? | Chat RAG | Embeddings + busca semântica + validação |
| Como evita alucinações? | Guardrails | Score de confiança, bloqueio se < 60 |
| Como monitora falhas? | Logging | Logs estruturados em JSON |
| Cuidados de segurança? | Revisão | JWT, RBAC, ownership enforcement |

---

## Notas para Gravação

- Falar naturalmente, não ler palavra por palavra
- Fazer pausas entre seções
- Manter tom profissional mas acessível
- Não mostrar credenciais ou chaves de API
- Usar documentos fictícios (já preparados)
- Ter planos alternativos prontos
- Cronometrar para validar duração

---

**Versão**: Otimizada  
**Duração**: ~8 minutos (970 palavras)  
**Status**: PRONTO PARA GRAVAÇÃO (após redução)
