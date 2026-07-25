# Color Reference — Legal AI Copilot

> Paleta de cores utilizada pela aplicação, documentada para referência na edição de vídeo.
> Todas as cores foram extraídas diretamente do código-fonte (TailwindCSS classes).

---

## 1. Cores Principais da Aplicação

### Fundo e Estrutura

| Elemento | Tailwind Class | Hex | Uso |
|----------|---------------|-----|-----|
| Fundo da página | `bg-gray-50` | #F9FAFB | Fundo geral de todas as páginas protegidas |
| Navbar | `bg-white` | #FFFFFF | Barra de navegação superior |
| Borda da navbar | `border-gray-200` | #E5E7EB | Borda inferior da navbar |
| Cards | `bg-white` | #FFFFFF | Fundo de todos os cards |
| Texto principal | `text-gray-900` | #111827 | Títulos, números, nomes |
| Texto secundário | `text-gray-700` | #374151 | Descrições, conteúdo |
| Texto terciário | `text-gray-500` | #6B7280 | Labels, metadados |
| Texto placeholder | `text-gray-400` | #9CA3AF | Estados vazios, aviso de estimativas |

### Cor de Destaque (Brand)

| Elemento | Tailwind Class | Hex | Uso |
|----------|---------------|-----|-----|
| Azul principal | `bg-blue-600` | #2563EB | Botão primário, logo, links |
| Azul hover | `bg-blue-700` | #1D4ED8 | Hover de botões |
| Azul claro | `bg-blue-50` | #EFF6FF | Fundo de credenciais demo, recomendações |
| Azul médio | `bg-blue-100` | #DBEAFE | Badge de role (LAWYER), barras de progresso |
| Azul texto | `text-blue-600` | #2563EB | Links, ícones |
| Azul escuro | `text-blue-900` | #1E3A8A | Texto em fundos blue-50 |

### Tela de Login

| Elemento | Tailwind Class | Hex | Uso |
|----------|---------------|-----|-----|
| Gradiente início | `from-blue-50` | #EFF6FF | Fundo da tela de login (topo) |
| Gradiente fim | `to-indigo-100` | #E0E7FF | Fundo da tela de login (base) |
| Logo container | `bg-blue-600` | #2563EB | Fundo do ícone Scale |
| Logo ícone | `text-white` | #FFFFFF | Ícone de balança |

---

## 2. Cores dos Riscos (Risk Analysis)

### Severity Badges

| Severidade | Tailwind Class (bg) | Tailwind Class (text) | Tailwind Class (border) | Hex (bg) | Hex (text) | Hex (border) |
|------------|---------------------|----------------------|------------------------|----------|------------|--------------|
| LOW | `bg-green-100` | `text-green-800` | `border-green-200` | #DCFCE7 | #166534 | #BBF7D0 |
| MEDIUM | `bg-yellow-100` | `text-yellow-800` | `border-yellow-200` | #FEF9C3 | #854D0E | #FEF08A |
| HIGH | `bg-orange-100` | `text-orange-800` | `border-orange-200` | #FFEDD5 | #9A3412 | #FED7AA |
| CRITICAL | `bg-red-100` | `text-red-800` | `border-red-200` | #FEE2E2 | #991B1B | #FECACA |

### Severity Border (RiskCard)

| Severidade | Tailwind Class (border-l-4) | Hex |
|------------|---------------------------|-----|
| LOW | `border-green-500` | #22C55E |
| MEDIUM | `border-yellow-500` | #EAB308 |
| HIGH | `border-orange-500` | #F97316 |
| CRITICAL | `border-red-500` | #EF4444 |

### Confidence Level

| Nível | Tailwind Class | Hex |
|-------|---------------|-----|
| High | `text-green-600` | #16A34A |
| Moderate | `text-yellow-600` | #CA8A04 |
| Low | `text-red-600` | #DC2626 |

### Overall Risk Card (cor de fundo conforme severidade)

| Severidade | Cor de fundo | Hex |
|------------|-------------|-----|
| Low | Verde | #DCFCE7 |
| Medium | Amarelo | #FEF9C3 |
| High | Laranja | #FFEDD5 |
| Critical | Vermelho | #FEE2E2 |

---

## 3. Cores dos Badges de Cláusulas (Analysis)

| Risco | Tailwind Class (bg) | Tailwind Class (text) | Hex (bg) | Hex (text) |
|-------|---------------------|----------------------|----------|------------|
| Baixo | `bg-green-100` | `text-green-800` | #DCFCE7 | #166534 |
| Médio | `bg-yellow-100` | `text-yellow-800` | #FEF9C3 | #854D0E |
| Alto | `bg-red-100` | `text-red-800` | #FEE2E2 | #991B1B |

### Border Color por Card de Extração

| Card | Ícone | Cor do ícone | Border color | Hex |
|------|-------|-------------|-------------|-----|
| Partes Envolvidas | Users | `text-blue-600` | `border-blue-500` | #3B82F6 |
| Datas Importantes | Calendar | `text-green-600` | `border-green-500` | #22C55E |
| Valores | DollarSign | `text-amber-600` | `border-amber-500` | #F59E0B |
| Cláusulas Importantes | Scale | `text-purple-600` | `border-purple-500` | #A855F7 |

---

## 4. Cores dos Status (Automações)

### Status Badges

| Status | Tailwind Class (bg) | Tailwind Class (text) | Hex (bg) | Hex (text) |
|--------|---------------------|----------------------|----------|------------|
| PENDING | `bg-gray-100` | `text-gray-700` | #F3F4F6 | #374151 |
| RUNNING | `bg-blue-100` | `text-blue-700` | #DBEAFE | #1D4ED8 |
| COMPLETED | `bg-green-100` | `text-green-700` | #DCFCE7 | #15803D |
| FAILED | `bg-red-100` | `text-red-700` | #FEE2E2 | #B91C1C |
| PARTIAL_SUCCESS | `bg-yellow-100` | `text-yellow-700` | #FEF9C3 | #A16207 |

### Progress Bar Colors

| Status | Tailwind Class | Hex |
|--------|---------------|-----|
| COMPLETED | `bg-green-500` | #22C55E |
| FAILED | `bg-red-500` | #EF4444 |
| PARTIAL_SUCCESS | `bg-yellow-500` | #EAB308 |
| PENDING / RUNNING | `bg-blue-500` | #3B82F6 |

### Webhook Status

| Status | Tailwind Class | Hex |
|--------|---------------|-----|
| sent | `text-green-600` | #16A34A |
| failed | `text-red-600` | #DC2626 |
| pending | `text-gray-600` | #4B5563 |

---

## 5. Cores dos Status (Revisões)

### Status Badges

| Status | Tailwind Class (bg) | Tailwind Class (text) | Hex (bg) | Hex (text) |
|--------|---------------------|----------------------|----------|------------|
| GENERATED | `bg-gray-100` | `text-gray-700` | #F3F4F6 | #374151 |
| PENDING_REVIEW | `bg-blue-100` | `text-blue-700` | #DBEAFE | #1D4ED8 |
| APPROVED | `bg-green-100` | `text-green-700` | #DCFCE7 | #15803D |
| REJECTED | `bg-red-100` | `text-red-700` | #FEE2E2 | #B91C1C |
| NEEDS_CHANGES | `bg-yellow-100` | `text-yellow-700` | #FEF9C3 | #A16207 |

### Decision Badges (Histórico)

| Decision | Tailwind Class (bg) | Tailwind Class (text) | Hex (bg) | Hex (text) |
|----------|---------------------|----------------------|----------|------------|
| APPROVE | `bg-green-100` | `text-green-700` | #DCFCE7 | #15803D |
| REJECT | `bg-red-100` | `text-red-700` | #FEE2E2 | #B91C1C |
| REQUEST_CHANGES | `bg-yellow-100` | `text-yellow-700` | #FEF9C3 | #A16207 |

---

## 6. Cores dos Cards de Métricas (Insights)

### Top Metrics Cards

| Card | Ícone | Cor do ícone | Hex |
|------|-------|-------------|-----|
| Documentos | FileText | `text-blue-600` | #2563EB |
| Análises Geradas | BarChart3 | `text-purple-600` | #9333EA |
| Tempo Poupado | TrendingUp | `text-green-600` | #16A34A |
| Taxa de Aprovação | CheckCircle | `text-green-600` | #16A34A |

### Grid 2x2 Headers

| Card | Ícone | Cor do ícone | Hex |
|------|-------|-------------|-----|
| Riscos por Severidade | Shield | `text-orange-500` | #F97316 |
| Automações por Status | Zap | `text-blue-500` | #3B82F6 |
| Estimativa de Produtividade | Clock | `text-blue-500` | #3B82F6 |

### Estimativa de Produtividade — Backgrounds

| Coluna | Tailwind Class (bg) | Tailwind Class (text) | Hex (bg) | Hex (text) |
|--------|---------------------|----------------------|----------|------------|
| Tempo Manual Estimado | `bg-blue-50` | `text-blue-900` | #EFF6FF | #1E3A8A |
| Tempo Poupado Estimado | `bg-green-50` | `text-green-900` | #F0FDF4 | #14532D |
| Confiança Média | `bg-purple-50` | `text-purple-900` | #FAF5FF | #581C87 |

### Barra de Progresso (Análises por Tipo)

| Elemento | Tailwind Class | Hex |
|----------|---------------|-----|
| Track | `bg-gray-200` | #E5E7EB |
| Fill | `bg-blue-500` | #3B82F6 |

---

## 7. Cores de Erro e Aviso

| Tipo | Tailwind Class (bg) | Tailwind Class (border) | Tailwind Class (text) | Hex (bg) | Hex (border) | Hex (text) |
|------|---------------------|------------------------|----------------------|----------|-------------|------------|
| Erro | `bg-red-50` | `border-red-200` | `text-red-700` | #FEF2F2 | #FECACA | #B91C1C |
| Aviso | `bg-yellow-50` | `border-yellow-200` | `text-yellow-700` | #FEFCE8 | #FEF08A | #A16207 |
| Sucesso | `bg-green-50` | `border-green-200` | `text-green-700` | #F0FDF4 | #BBF7D0 | #15803D |
| Informação | `bg-blue-50` | `border-blue-200` | `text-blue-900` | #EFF6FF | #BFDBFE | #1E3A8A |

---

## 8. Paleta Resumida para o Editor

### Cores Primárias (Brand)

| Nome | Hex | Uso no vídeo |
|------|-----|-------------|
| Azul principal | #2563EB | Callouts, links, elementos de destaque |
| Azul claro | #EFF6FF | Fundos suaves |
| Branco | #FFFFFF | Texto overlaid, cards |
| Cinza escuro | #111827 | Texto principal |
| Cinza médio | #6B7280 | Texto secundário |
| Cinza claro | #F9FAFB | Fundo da aplicação |

### Cores de Status (semáforo)

| Nome | Hex | Uso |
|------|-----|-----|
| Verde | #22C55E | Sucesso, aprovado, low risk |
| Amarelo | #EAB308 | Aviso, parcial, medium risk |
| Laranja | #F97316 | High risk |
| Vermelho | #EF4444 | Erro, rejeitado, critical risk |

### Cores dos Cards de Extração

| Nome | Hex | Card |
|------|-----|------|
| Azul | #3B82F6 | Partes Envolvidas |
| Verde | #22C55E | Datas Importantes |
| Amber | #F59E0B | Valores |
| Roxo | #A855F7 | Cláusulas Importantes |

### Cor do End Credits

| Nome | Hex | Uso |
|------|-----|-----|
| Slate-900 | #0F172A | Fundo dos end credits |
| Slate-400 | #94A3B8 | Subtítulo dos end credits |
| Slate-500 | #64748B | Tecnologias nos end credits |
