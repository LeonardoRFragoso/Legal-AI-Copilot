# Icon Reference — Legal AI Copilot

> Lista de todos os ícones utilizados na aplicação, extraídos do código-fonte.
> Biblioteca: Lucide React (lucide-react).
> Referência para o editor: saber quais ícones aparecem e quando destacá-los.

---

## 1. Ícones por Página

### Login (`Login.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| ⚖️ | Scale | Logo da balança no topo da tela de login | Cena 01 — cursor para sobre o logo |
| 🔒 | Lock | Ícone ao lado do título "Legal AI Copilot" | Não destacar |
| 👤 | User | Ícone ao lado do campo de email | Não destacar |
| 🔑 | KeyRound | Ícone ao lado do campo de senha | Não destacar |

### Layout / Navbar (`Layout.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| ⚖️ | Scale | Logo na navbar (canto esquerdo) | Não destacar individualmente |
| 📊 | LayoutDashboard | Item "Dashboard" na navbar | Cena 05 — cursor para sobre cada item |
| 📤 | Upload | Item "Upload" na navbar | Cena 05 — cursor para sobre cada item |
| 💬 | MessageSquare | Item "Chat" na navbar | Cena 05 — cursor para sobre cada item |
| 📄 | FileSearch | Item "Análise" na navbar | Cena 05 — cursor para sobre cada item |
| 🛡️ | Shield | Item "Riscos" na navbar | Cena 05 — cursor para sobre cada item |
| ⚡ | Zap | Item "Automações" na navbar | Cena 05 — cursor para sobre cada item |
| ✅ | CheckCircle | Item "Revisões" na navbar | Cena 05 — cursor para sobre cada item |
| 📈 | BarChart3 | Item "Métricas" na navbar | Cena 05 — cursor para sobre cada item |
| 🔄 | GitCompare | Item "Comparação" na navbar | Cena 05 — cursor para sobre cada item |
| 🚪 | LogOut | Botão de logout (canto direito) | Não destacar |

### Dashboard (`Dashboard.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| 📄 | FileText | Em cada card de documento | Cena 05 — cursor para sobre o card |
| ✅ | CheckCircle | Badge "Ready" no card de documento | Cena 05 — status do documento |
| ⏳ | Clock | Badge "Processing" no card de documento | Não destacar (se documento estiver pronto) |
| 💬 | MessageSquare | Botão "Chat" no card de documento | Não destacar |
| 📄 | FileSearch | Botão "Análise" no card de documento | Cena 05 — cursor para sobre o botão |
| 🗑️ | Trash2 | Botão "Delete" no card de documento | Não destacar |
| ➕ | Plus | Botão "Upload PDF" no canto superior direito | Cena 05 — cursor para antes de clicar |

### Upload (`Upload.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| 📤 | Upload | Área de drop zone | Cena 06 — cursor para sobre a área |
| ✅ | CheckCircle | Tela de sucesso após upload | Cena 06 — tela de sucesso visível por 3s |

### Analysis (`Analysis.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| 📝 | FileText | Header do card de Resumo | Cena 07 — cursor para sobre o card |
| 👥 | Users | Header do card "Partes Envolvidas" | Cena 07 — cursor para sobre o card |
| 📅 | Calendar | Header do card "Datas Importantes" | Cena 07 — cursor para sobre o card |
| 💰 | DollarSign | Header do card "Valores" | Cena 07 — cursor para sobre o card |
| ⚖️ | Scale | Header do card "Cláusulas Importantes" | Cena 07 — cursor para sobre o card |
| 💬 | MessageSquare | Botão "Iniciar Chat" | Cena 07 — cursor para antes de clicar |
| ⏳ | Loader2 | Loading spinner durante análise | Não destacar (aguardar) |

### Chat (`Chat.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| ➕ | Plus | Botão "Nova Conversa" na sidebar | Cena 08 — cursor para sobre o botão |
| 📤 | SendHorizontal | Botão Send ao lado do campo de texto | Cena 08 — cursor para antes de clicar |
| ⚠️ | AlertTriangle | RiskBadge na resposta estruturada | Cena 08 — callout na resposta |
| 📄 | FileText | Citação — ícone de documento | Cena 08 — cursor para sobre citações |
| 🛡️ | Shield | Disclaimer jurídico | Cena 08 — callout no disclaimer |

### Risk Analysis (`RiskAnalysis.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| ⚠️ | AlertTriangle | Overall risk card (severidade alta) | Cena 09 — callout no overall risk |
| 🛡️ | Shield | Overall risk card (severidade baixa) | Cena 09 — callout no overall risk |
| 📄 | FileText | Header da página de riscos | Não destacar |
| ⬇️ | ChevronDown | Botão "Sources" (expansível) | Cena 09 — cursor para antes de clicar |
| ⬆️ | ChevronUp | Botão "Sources" (recolher) | Não destacar (após expandir) |

### Automations (`Automations.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| ⚡ | Zap | Header da página + ícone de run | Cena 10 — cursor para sobre o card |
| ✅ | CheckCircle | Status badge COMPLETED | Cena 10 — callout no status |
| ❌ | XCircle | Status badge FAILED | Cena 10 — callout no status |
| ⏳ | Clock | Status badge PENDING | Cena 10 — callout no status |
| ⚠️ | AlertCircle | Status badge PARTIAL_SUCCESS | Cena 10 — callout no status |
| 🔄 | RefreshCw | Botão "Atualizar" + botão "Tentar Novamente" | Cena 10 — cursor para sobre o botão |

### Reviews (`Reviews.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| ✅ | CheckCircle | Status APPROVED + botão "Aprovar" | Cena 11 — callout no botão |
| ❌ | XCircle | Status REJECTED + botão "Rejeitar" | Cena 11 — callout no botão |
| ⚠️ | AlertCircle | Status NEEDS_CHANGES + botão "Correções" | Cena 11 — callout no botão |
| ⏳ | Clock | Status GENERATED | Cena 11 — cursor para sobre o card |
| 🔍 | FileSearch | Header da página | Não destacar |
| 🛡️ | Shield | Ícone de risk analysis | Não destacar |
| ➡️ | ChevronRight | Indicador de seleção na lista | Não destacar |
| ✖️ | X | Botão de fechar painel de detalhe | Não destacar |
| 🔒 | Lock | Indicador de permissão (se não for ADMIN/LAWYER) | Não destacar (usar perfil LAWYER) |

### Insights (`Insights.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| 📄 | FileText | Card "Documentos" | Cena 12 — callout nos 4 cards |
| 📊 | BarChart3 | Card "Análises Geradas" | Cena 12 — callout nos 4 cards |
| 📈 | TrendingUp | Card "Tempo Poupado" | Cena 12 — callout nos 4 cards |
| ✅ | CheckCircle | Card "Taxa de Aprovação" | Cena 12 — callout nos 4 cards |
| 🛡️ | Shield | Header "Riscos por Severidade" | Cena 12 — cursor para sobre o card |
| ⚡ | Zap | Header "Automações por Status" | Cena 12 — cursor para sobre o card |
| ⏰ | Clock | Header "Estimativa de Produtividade" | Cena 12 — cursor para sobre a estimativa |
| 🔄 | RefreshCw | Botão "Atualizar" | Não destacar |

### Comparison (`Comparison.tsx`)

| Ícone | Nome Lucide | Onde aparece | Quando destacar |
|-------|-------------|-------------|-----------------|
| 🔄 | GitCompare | Header da página | Não destacar |
| 📄 | FileText | Ícone ao lado dos dropdowns | Não destacar |

---

## 2. Ícones de Status — Resumo Visual

### Risk Severity

| Severidade | Ícone | Cor | Hex |
|------------|-------|-----|-----|
| LOW | Shield / CheckCircle | Verde | #22C55E |
| MEDIUM | AlertTriangle | Amarelo | #EAB308 |
| HIGH | AlertTriangle | Laranja | #F97316 |
| CRITICAL | AlertTriangle | Vermelho | #EF4444 |

### Automation Status

| Status | Ícone | Cor do badge | Hex (bg) |
|--------|-------|-------------|----------|
| PENDING | Clock | Cinza | #F3F4F6 |
| RUNNING | Zap | Azul | #DBEAFE |
| COMPLETED | CheckCircle | Verde | #DCFCE7 |
| FAILED | XCircle | Vermelho | #FEE2E2 |
| PARTIAL_SUCCESS | AlertCircle | Amarelo | #FEF9C3 |

### Review Status

| Status | Ícone | Cor do badge | Hex (bg) |
|--------|-------|-------------|----------|
| GENERATED | Clock | Cinza | #F3F4F6 |
| PENDING_REVIEW | AlertCircle | Azul | #DBEAFE |
| APPROVED | CheckCircle | Verde | #DCFCE7 |
| REJECTED | XCircle | Vermelho | #FEE2E2 |
| NEEDS_CHANGES | AlertCircle | Amarelo | #FEF9C3 |

---

## 3. Quando Destacar Ícones

### Alta Prioridade (sempre destacar)

| Ícone | Cena | Razão |
|-------|------|-------|
| Scale (logo) | 01 | Identidade visual do projeto |
| CheckCircle (sucesso upload) | 06 | Confirmação de ação bem-sucedida |
| AlertTriangle (risk badge no chat) | 08 | Guardrails — resposta estruturada |
| Shield (disclaimer no chat) | 08 | Guardrails — transparência |
| AlertTriangle (overall risk) | 09 | Resultado principal da análise |
| ChevronDown (Sources) | 09 | Rastreabilidade — expandir citações |
| CheckCircle (botão Aprovar) | 11 | Ação de revisão humana |
| FileText (card Documentos) | 12 | Métrica principal |
| BarChart3 (card Análises) | 12 | Métrica principal |
| TrendingUp (card Tempo Poupado) | 12 | Métrica principal |

### Média Prioridade (destacar se tempo permitir)

| Ícone | Cena | Razão |
|-------|------|-------|
| Users (Partes) | 07 | Extração estruturada |
| Calendar (Datas) | 07 | Extração estruturada |
| DollarSign (Valores) | 07 | Extração estruturada |
| Scale (Cláusulas) | 07 | Extração estruturada |
| Zap (status RUNNING) | 10 | Pipeline em execução |
| CheckCircle (status COMPLETED) | 10 | Pipeline concluído |
| Shield (Riscos por Severidade) | 12 | Visualização de métricas |
| Zap (Automações por Status) | 12 | Visualização de métricas |

### Baixa Prioridade (não destacar)

| Ícone | Cena | Razão |
|-------|------|-------|
| Lock, User, KeyRound | 01, 04 | Decorativos no login |
| LayoutDashboard, Upload, etc. (navbar) | 05 | Cursor já passa por todos |
| Trash2 | 05 | Ação destrutiva — não demonstrar |
| LogOut | Todas | Não relevante para a demo |
| Loader2 (spinner) | 07, 08, 09 | Estado temporário — aguardar |
| RefreshCw | 10, 12 | Ação secundária |
| X (fechar painel) | 11 | Ação secundária |
| ChevronRight | 11 | Indicador decorativo |
