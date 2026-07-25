# Screen Callouts — Legal AI Copilot

> Destaques visuais sobre elementos específicos da tela durante a demonstração.
> Estilo: retângulo sutil com borda azul, sem preenchimento. Ou zoom digital.
> Referência: Stripe, Vercel, Linear.

---

## Especificações Técnicas Gerais

### Retângulo de Destaque

| Parâmetro | Valor |
|-----------|-------|
| Cor da borda | #3B82F6 (blue-500) |
| Espessura da borda | 2px |
| Raio da borda | 4px |
| Preenchimento | Transparente (0% opacidade) |
| Opacidade da borda | 80% |
| Animação de entrada | Fade in 0.3s |
| Animação de saída | Fade out 0.3s |
| Duração mínima | 2s |
| Duração máxima | 5s |

### Zoom Digital

| Parâmetro | Valor |
|-----------|-------|
| Zoom máximo | 115% |
| Zoom recomendado | 105–110% |
| Animação de entrada | Ease in 0.5s |
| Animação de saída | Ease out 0.5s |
| Duração mínima | 2s |

---

## Callouts por Cena

### Cena 05 — Dashboard

#### Callout 05-A: Navbar

| Campo | Valor |
|------|-------|
| **Elemento** | Barra de navegação (9 itens) |
| **Forma** | Retângulo de destaque |
| **Posição** | Topo da tela, largura total (x:0, y:0, w:1920, h:64) |
| **Duração** | 3s |
| **Momento** | Quando o cursor percorre a navbar |
| **Motivo** | Mostrar a amplitude do sistema — 9 funcionalidades acessíveis |

#### Callout 05-B: Role Badge

| Campo | Valor |
|------|-------|
| **Elemento** | Nome do usuário + role badge (LAWYER) |
| **Forma** | Zoom digital 105% |
| **Posição** | Canto superior direito (x:1750, y:32) |
| **Duração** | 2s |
| **Momento** | Quando o cursor para sobre o nome/role |
| **Motivo** | Destacar RBAC — controle de acesso por papéis |

---

### Cena 07 — Análise

#### Callout 07-A: Card de Resumo

| Campo | Valor |
|------|-------|
| **Elemento** | Card de Resumo (texto gerado automaticamente) |
| **Forma** | Zoom digital 105% |
| **Posição** | Centro superior (x:960, y:250) |
| **Duração** | 3s |
| **Momento** | Quando o resumo aparece após loading |
| **Motivo** | Mostrar o resultado da geração automática de resumo |

#### Callout 07-B: Badges de Risco nas Cláusulas

| Campo | Valor |
|------|-------|
| **Elemento** | Badges "Baixo Risco" / "Risco Médio" / "Alto Risco" no card de Cláusulas |
| **Forma** | Zoom digital 110% |
| **Posição** | Card de Cláusulas Importantes (x:1400, y:800) |
| **Duração** | 3s |
| **Momento** | Quando o cursor passa sobre os badges |
| **Motivo** | Destacar classificação de risco por cláusula — diferencial visual |

---

### Cena 08 — Chat

#### Callout 08-A: Resposta Estruturada

| Campo | Valor |
|------|-------|
| **Elemento** | Resposta do assistente com RiskBadge, título, descrição e recomendação |
| **Forma** | Zoom digital 110% |
| **Posição** | Balão de resposta do assistente (x:800, y:600) |
| **Duração** | 3s |
| **Momento** | Quando a resposta aparece após loading |
| **Motivo** | Mostrar o resultado do agent router — resposta estruturada |

#### Callout 08-B: Citações

| Campo | Valor |
|------|-------|
| **Elemento** | Citações abaixo da resposta (document_title, page number, excerpt, similarity) |
| **Forma** | Retângulo de destaque |
| **Posição** | Área de citações (x:600, y:750, w:600, h:120) |
| **Duração** | 3s |
| **Momento** | Quando o cursor para sobre as citações |
| **Motivo** | Destacar guardrails — citações obrigatórias com rastreabilidade |

#### Callout 08-C: Disclaimer

| Campo | Valor |
|------|-------|
| **Elemento** | Disclaimer jurídico em itálico cinza claro |
| **Forma** | Retângulo de destaque |
| **Posição** | Disclaimer ao final (x:600, y:880, w:600, h:40) |
| **Duração** | 3s |
| **Momento** | Quando o cursor para sobre o disclaimer |
| **Motivo** | Destacar guardrails — disclaimer jurídico obrigatório |

---

### Cena 09 — Riscos

#### Callout 09-A: Overall Risk Card

| Campo | Valor |
|------|-------|
| **Elemento** | Card de Overall Risk (número grande, confidence score, level) |
| **Forma** | Zoom digital 110% |
| **Posição** | Overall risk card (x:960, y:300) |
| **Duração** | 3s |
| **Momento** | Quando o resultado aparece após loading |
| **Motivo** | Mostrar o resultado principal da análise de riscos |

#### Callout 09-B: Severity Badge

| Campo | Valor |
|------|-------|
| **Elemento** | Badge de severidade (LOW/MEDIUM/HIGH/CRITICAL) no primeiro risk card |
| **Forma** | Retângulo de destaque |
| **Posição** | Badge no risk card (x:300, y:500, w:100, h:28) |
| **Duração** | 2s |
| **Momento** | Quando o cursor para sobre o risk card |
| **Motivo** | Destacar classificação de severidade — diferencial visual |

#### Callout 09-C: Sources Expandidas

| Campo | Valor |
|------|-------|
| **Elemento** | Sources expandidas (excerpt, page number, similarity score) |
| **Forma** | Retângulo de destaque |
| **Posição** | Área de sources (x:400, y:650, w:800, h:100) |
| **Duração** | 3s |
| **Momento** | Após clicar "Sources" e expandir |
| **Motivo** | Destacar rastreabilidade — trecho exato do documento que motivou o risco |

#### Callout 09-D: Disclaimer (Heurística)

| Campo | Valor |
|------|-------|
| **Elemento** | Disclaimer ao final da página de riscos |
| **Forma** | Retângulo de destaque |
| **Posição** | Disclaimer (x:400, y:880, w:800, h:40) |
| **Duração** | 3s |
| **Momento** | Quando o cursor para sobre o disclaimer |
| **Motivo** | Destacar limitação consciente — análise heurística sem LLM |

---

### Cena 10 — Automações

#### Callout 10-A: Status Badge

| Campo | Valor |
|------|-------|
| **Elemento** | Status badge (COMPLETED/FAILED/PARTIAL_SUCCESS) no primeiro run |
| **Forma** | Zoom digital 105% |
| **Posição** | Status badge (x:300, y:300) |
| **Duração** | 2s |
| **Momento** | Quando o cursor para sobre o status |
| **Motivo** | Mostrar o funcionamento do pipeline de automação |

#### Callout 10-B: Barra de Progresso

| Campo | Valor |
|------|-------|
| **Elemento** | Barra de progresso com percentual |
| **Forma** | Retângulo de destaque |
| **Posição** | Barra de progresso (x:200, y:340, w:800, h:24) |
| **Duração** | 2s |
| **Momento** | Quando o cursor para sobre a barra |
| **Motivo** | Mostrar progresso do pipeline em background |

#### Callout 10-C: Webhook Status

| Campo | Valor |
|------|-------|
| **Elemento** | Webhook status (sent/failed/pending) |
| **Forma** | Retângulo de destaque |
| **Posição** | Webhook status (x:1300, y:350, w:150, h:24) |
| **Duração** | 2s |
| **Momento** | Quando o cursor para sobre o webhook |
| **Motivo** | Destacar integração com n8n via webhook |

---

### Cena 11 — Revisões

#### Callout 11-A: Status Badge na Lista

| Campo | Valor |
|------|-------|
| **Elemento** | Status badge (Gerada/Pendente/Aprovada/Rejeitada/Correções) no card da lista |
| **Forma** | Zoom digital 105% |
| **Posição** | Status badge no card (x:200, y:250) |
| **Duração** | 2s |
| **Momento** | Quando o cursor para sobre o primeiro card |
| **Motivo** | Mostrar a state machine de revisão |

#### Callout 11-B: Histórico de Revisões

| Campo | Valor |
|------|-------|
| **Elemento** | Histórico de revisões (decision, reviewer, comment, date) |
| **Forma** | Retângulo de destaque |
| **Posição** | Área do histórico (x:600, y:550, w:800, h:120) |
| **Duração** | 3s |
| **Momento** | Quando o cursor para sobre o histórico |
| **Motivo** | Destacar trilha de auditoria append-only |

#### Callout 11-C: Botões de Revisão

| Campo | Valor |
|------|-------|
| **Elemento** | Três botões: Aprovar / Rejeitar / Correções |
| **Forma** | Retângulo de destaque |
| **Posição** | Área dos botões (x:600, y:830, w:500, h:40) |
| **Duração** | 2s |
| **Momento** | Antes de clicar "Aprovar" |
| **Motivo** | Mostrar o formulário de revisão humana |

---

### Cena 12 — Métricas

#### Callout 12-A: 4 Cards Superiores

| Campo | Valor |
|------|-------|
| **Elemento** | Cards de Documentos, Análises, Tempo Poupado, Taxa de Aprovação |
| **Forma** | Retângulo de destaque |
| **Posição** | Largura dos 4 cards (x:80, y:180, w:1760, h:120) |
| **Duração** | 3s |
| **Momento** | Quando os 4 cards estão visíveis |
| **Motivo** | Mostrar métricas principais de produtividade |

#### Callout 12-B: Aviso de Estimativas

| Campo | Valor |
|------|-------|
| **Elemento** | Aviso em itálico (estimation_notice) |
| **Forma** | Retângulo de destaque |
| **Posição** | Aviso (x:400, y:1000, w:800, h:30) |
| **Duração** | 3s |
| **Momento** | Quando o cursor para sobre o aviso |
| **Motivo** | Destacar transparência — estimativas do MVP, não calibradas |

---

### Cena 13 — Comparação

#### Callout 13-A: Resultado da Comparação

| Campo | Valor |
|------|-------|
| **Elemento** | Card com "Resultado da Comparação" (texto formatado com bold) |
| **Forma** | Zoom digital 105% |
| **Posição** | Card de resultado (x:960, y:600) |
| **Duração** | 3s |
| **Momento** | Quando o resultado aparece após loading |
| **Motivo** | Mostrar o resultado da comparação lado a lado |

---

## Resumo

| ID | Cena | Elemento | Forma | Duração |
|----|------|----------|-------|---------|
| 05-A | 05 | Navbar | Retângulo | 3s |
| 05-B | 05 | Role badge | Zoom 105% | 2s |
| 07-A | 07 | Card de resumo | Zoom 105% | 3s |
| 07-B | 07 | Badges de risco | Zoom 110% | 3s |
| 08-A | 08 | Resposta estruturada | Zoom 110% | 3s |
| 08-B | 08 | Citações | Retângulo | 3s |
| 08-C | 08 | Disclaimer | Retângulo | 3s |
| 09-A | 09 | Overall risk | Zoom 110% | 3s |
| 09-B | 09 | Severity badge | Retângulo | 2s |
| 09-C | 09 | Sources | Retângulo | 3s |
| 09-D | 09 | Disclaimer | Retângulo | 3s |
| 10-A | 10 | Status badge | Zoom 105% | 2s |
| 10-B | 10 | Barra de progresso | Retângulo | 2s |
| 10-C | 10 | Webhook status | Retângulo | 2s |
| 11-A | 11 | Status badge | Zoom 105% | 2s |
| 11-B | 11 | Histórico | Retângulo | 3s |
| 11-C | 11 | Botões de revisão | Retângulo | 2s |
| 12-A | 12 | 4 cards superiores | Retângulo | 3s |
| 12-B | 12 | Aviso de estimativas | Retângulo | 3s |
| 13-A | 13 | Resultado | Zoom 105% | 3s |

> **Total**: 20 callouts em 8 cenas. Cenas 01–04, 06 e 14 não recebem callouts.
